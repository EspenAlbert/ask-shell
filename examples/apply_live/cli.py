from __future__ import annotations

import logging
from pathlib import Path

import typer

from apply_live.stream_handler import PlanStreamHandler, plan_stream_callback
from ask_shell import console
from ask_shell.shell import run_and_wait

logger = logging.getLogger(__name__)

app = typer.Typer(
    name="apply-live",
    help="Demo terraform apply -json streaming with ask-shell live rendering.",
)

_DEFAULT_WORKSPACE = Path(__file__).resolve().parent / "workspace"


def _run_terraform(command: str, *, workspace: Path) -> int:
    run = run_and_wait(
        command,
        cwd=workspace,
        allow_non_zero_exit=True,
        skip_progress_output=True,
    )
    return run.exit_code or 0


def _terraform_init(*, workspace: Path) -> None:
    logger.info("running terraform init")
    if (exit_code := _run_terraform("terraform init -input=false", workspace=workspace)) != 0:
        raise typer.Exit(exit_code)
    logger.info("terraform init complete")


@app.command()
def apply(
    workspace: Path = typer.Option(
        _DEFAULT_WORKSPACE,
        "--workspace",
        "-w",
        help="Terraform workspace with chained time_sleep resources.",
        exists=True,
        file_okay=False,
    ),
) -> None:
    _terraform_init(workspace=workspace)

    handler = PlanStreamHandler()
    callback = plan_stream_callback(handler)
    run = run_and_wait(
        "terraform apply -json -auto-approve",
        cwd=workspace,
        allow_non_zero_exit=True,
        skip_progress_output=True,
        message_callbacks=[callback],
    )
    handler.flush()
    if (exit_code := run.exit_code or 0) != 0:
        raise typer.Exit(exit_code)
    logger.info("apply complete")


def main() -> None:
    console.configure_logging(app)
    app()


if __name__ == "__main__":
    main()
