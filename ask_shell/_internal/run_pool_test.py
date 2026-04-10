from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread
from unittest.mock import MagicMock, patch

from ask_shell._internal._run import get_pool, max_run_count_for_workers, wait_if_many_runs
from ask_shell._internal.rich_progress import new_task
from ask_shell._internal.run_pool import run_pool

_module = run_pool.__module__


def test_run_pool_dedicated_pool():
    with patch(f"{_module}.{max_run_count_for_workers.__name__}", return_value=10):
        rp = run_pool(task_name="test", pool_thread_count=8, max_concurrent_submits=2)

    assert rp._owns_pool
    assert rp._pool_max_workers == 8
    assert rp._max_run_count_with_this_pool == 8  # global_max_runs(10) - runs_needed(2)
    rp.pool.shutdown(wait=False)


def test_run_pool_shared_pool():
    mock_pool = MagicMock(spec=ThreadPoolExecutor)
    mock_pool._max_workers = 20
    with patch(f"{_module}.{get_pool.__name__}", return_value=mock_pool):
        rp = run_pool(task_name="test", max_concurrent_submits=2, threads_used_per_submit=4)

    assert not rp._owns_pool
    assert rp._pool_max_workers == 20
    # max_run_count_for_workers(20) = 20 // 4 = 5
    # workers_required_if_full = 2 * 4 = 8, ceil(8/4) = 2
    assert rp._max_run_count_with_this_pool == 3  # 5 - 2


def test_run_pool_exit_shuts_down_owned_pool():
    with patch(f"{_module}.{max_run_count_for_workers.__name__}", return_value=10):
        rp = run_pool(task_name="test", pool_thread_count=8, max_concurrent_submits=2)

    real_pool = rp.pool
    mock_pool = MagicMock(spec=ThreadPoolExecutor)
    rp.pool = mock_pool
    real_pool.shutdown(wait=False)

    mock_task = MagicMock(spec=new_task)
    rp._task = mock_task

    done_future = Future()
    done_future.set_result("ok")
    rp._futures.append(done_future)

    rp.__exit__(None, None, None)

    mock_pool.shutdown.assert_called_once_with(wait=True)
    mock_task.__exit__.assert_called_once_with(None, None, None)


def test_run_pool_exit_no_submits_does_not_block():
    """__exit__ returns immediately when no tasks were submitted."""
    mock_pool = MagicMock(spec=ThreadPoolExecutor)
    mock_pool._max_workers = 20
    with patch(f"{_module}.{get_pool.__name__}", return_value=mock_pool):
        rp = run_pool(task_name="no-submits", max_concurrent_submits=2, threads_used_per_submit=4)

    mock_task = MagicMock(spec=new_task)
    rp._task = mock_task

    completed = False

    def call_exit():
        nonlocal completed
        rp.__exit__(None, None, None)
        completed = True

    t = Thread(target=call_exit)
    t.start()
    t.join(timeout=2)
    assert completed, "__exit__ blocked despite no submits"


def test_run_pool_submit_and_exit():
    """submit() stores futures and __exit__ waits on them."""
    results: list[str] = []

    def task_fn():
        results.append("done")
        return "ok"

    mock_pool = MagicMock(spec=ThreadPoolExecutor)
    mock_pool._max_workers = 20
    mock_pool.submit = MagicMock(side_effect=lambda fn, *a, **kw: _immediate_future(fn, *a, **kw))

    with patch(f"{_module}.{get_pool.__name__}", return_value=mock_pool):
        rp = run_pool(task_name="single", total=1, max_concurrent_submits=1, threads_used_per_submit=4, sleep_time=0.01)

    completed = False

    def do_submit():
        nonlocal completed
        mock_task = MagicMock(spec=new_task)
        rp._task = mock_task
        with patch(f"{_module}.{wait_if_many_runs.__name__}"):
            rp.submit(task_fn)
        assert len(rp._futures) == 1
        rp.__exit__(None, None, None)
        completed = True

    t = Thread(target=do_submit)
    t.start()
    t.join(timeout=5)
    assert completed, "submit() + __exit__ deadlocked"
    assert results == ["done"]


def test_run_pool_multiple_submits_and_exit():
    """Multiple submit() calls accumulate futures and __exit__ waits for all."""
    results: list[int] = []

    def task_fn(index: int):
        results.append(index)
        return index

    mock_pool = MagicMock(spec=ThreadPoolExecutor)
    mock_pool._max_workers = 20
    mock_pool.submit = MagicMock(side_effect=lambda fn, *a, **kw: _immediate_future(fn, *a, **kw))

    with patch(f"{_module}.{get_pool.__name__}", return_value=mock_pool):
        rp = run_pool(task_name="multi", total=3, max_concurrent_submits=3, threads_used_per_submit=4, sleep_time=0.01)

    completed = False

    def do_submits():
        nonlocal completed
        mock_task = MagicMock(spec=new_task)
        rp._task = mock_task
        with patch(f"{_module}.{wait_if_many_runs.__name__}"):
            for i in range(3):
                rp.submit(task_fn, i)
        assert len(rp._futures) == 3
        rp.__exit__(None, None, None)
        completed = True

    t = Thread(target=do_submits)
    t.start()
    t.join(timeout=5)
    assert completed, "multiple submit() + __exit__ deadlocked"
    assert sorted(results) == [0, 1, 2]


def _immediate_future(fn, *args, **kwargs):
    """Run fn synchronously and return a resolved Future with done callbacks."""
    fut = Future()
    try:
        result = fn(*args, **kwargs)
        fut.set_result(result)
    except Exception as e:
        fut.set_exception(e)
    return fut
