import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent.futures import wait as futures_wait
from dataclasses import dataclass, field
from math import ceil
from threading import RLock
from typing import Any, Callable, Protocol, TypeVar

from ask_shell._internal._run import (
    THREADS_PER_RUN,
    get_pool,
    handle_interrupt_wait,
    max_run_count_for_workers,
    wait_if_many_runs,
)
from ask_shell._internal.rich_progress import new_task
from ask_shell.settings import AskShellSettings

logger = logging.getLogger(__name__)
T_co = TypeVar("T_co", covariant=True)


class SubmitFunc(Protocol[T_co]):
    def __call__(self, *args: Any, **kwargs: Any) -> T_co: ...


@dataclass
class run_pool:
    task_name: str
    total: int = 0
    max_concurrent_submits: int = field(default=4)
    threads_used_per_submit: int = (
        THREADS_PER_RUN + 1
    )  # If you are using `run` or `run_and_wait` this should be `THREADS_PER_RUN` + extra threads for your own tasks
    pool_thread_count: int | None = None
    sleep_time: float = 1
    sleep_callback: Callable[[], Any] | None = None
    exit_wait_timeout: float | None = (
        None  # If set, will wait for the pool to finish before exiting the context manager
    )

    pool: ThreadPoolExecutor = field(init=False)
    _owns_pool: bool = field(init=False, default=False)
    _pool_max_workers: int = field(init=False)
    _max_run_count_with_this_pool: int = field(init=False)
    _lock: RLock = field(init=False, default_factory=RLock)
    _pending_count: int = field(init=False, default=0)
    _task: new_task | None = field(init=False, default=None)
    _futures: list[Future] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self.pool_thread_count is not None:
            self.pool = ThreadPoolExecutor(max_workers=self.pool_thread_count)
            self._owns_pool = True
            self._pool_max_workers = self.pool_thread_count
            # dedicated pool: each concurrent submit reserves 1 run slot on the global pool
            runs_needed = self.max_concurrent_submits
            runs_available = max_run_count_for_workers()
            logger.debug(
                f"run_pool '{self.task_name}': dedicated pool with {self.pool_thread_count} workers, "
                f"global pool reserves {runs_needed}/{runs_available} run slots"
            )
        else:
            self.pool = get_pool()
            self._pool_max_workers = self.pool._max_workers
            # shared pool: submits + their shell runs share the same threads
            workers_at_full_load = self.max_concurrent_submits * self.threads_used_per_submit
            runs_needed = ceil(workers_at_full_load / THREADS_PER_RUN)
            runs_available = max_run_count_for_workers(self._pool_max_workers)

        assert runs_needed < runs_available, (
            f"Run slots needed ({runs_needed}) exceed capacity ({runs_available}). "
            f"Adjust {AskShellSettings.ENV_NAME_THREAD_COUNT} or decrease `max_concurrent_submits`."
        )
        self._max_run_count_with_this_pool = runs_available - runs_needed

    def _on_submit_done(self, _future: Future):
        with self._lock:
            self._pending_count -= 1
            if task := self._task:
                task.update(advance=1)

    def submit(self, fn: SubmitFunc[T_co], /, *args, **kwargs) -> Future[T_co]:
        """Submit a task to the pool. Blocks if max_concurrent_submits are already in flight."""
        with self._lock:
            self._pending_count += 1
        with handle_interrupt_wait(interrupt_message=f"run_pool submit for {self.task_name}"):
            while self._pending_count > self.max_concurrent_submits:
                if self.sleep_callback:
                    self.sleep_callback()
                time.sleep(self.sleep_time)
        wait_if_many_runs(
            max_run_count=self._max_run_count_with_this_pool,
            sleep_time=self.sleep_time,
            sleep_callback=self.sleep_callback,
        )
        future = self.pool.submit(fn, *args, **kwargs)
        future.add_done_callback(self._on_submit_done)
        with self._lock:
            self._futures.append(future)
        return future

    def __enter__(self):
        self._task = new_task(self.task_name, self.total)
        self._task.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        with self._lock:
            futures = list(self._futures)
        if futures:
            with handle_interrupt_wait(interrupt_message=f"interrupt in `run_pool` exit method for {self.task_name}"):
                futures_wait(futures, timeout=self.exit_wait_timeout)
            with self._lock:
                self._futures.clear()

        if self._owns_pool:
            self.pool.shutdown(wait=True)
        if task := self._task:
            task.__exit__(exc_type, exc_value, traceback)
