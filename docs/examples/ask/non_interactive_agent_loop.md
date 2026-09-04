<!--
description: Dump, edit, and re-run a non-interactive prompt session
-->
# non_interactive_agent_loop

When a CLI runs without a TTY, `confirm` and `text` raise `NonInteractivePromptError` and write `non_interactive_prompt.yaml`. An agent edits `response` on each row and re-runs the same command until it succeeds. Replay follows `questions` index order; `session.command` and `session.pinned` keep the file across subprocess runs.

```python
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from model_lib import dump, parse
from model_lib.constants import FileFormat
from zero_3rdparty import file_utils

from ask_shell.settings import AskShellSettings

APP_SCRIPT = """\
import typer
from ask_shell.ask import confirm, text
from ask_shell.console import configure_logging, disable_interactive_shell
from ask_shell.settings import AskShellSettings

disable_interactive_shell()
settings = AskShellSettings.from_env(log_level="CRITICAL")
app = typer.Typer(name="demo")

@app.command()
def release() -> None:
    shipped = confirm("Ship it?")
    name = text("Release name?")
    print(f"shipped={shipped} name={name}")

configure_logging(app, settings=settings, skip_except_hook=True)
try:
    app()
except typer.Exit as exc:
    raise SystemExit(exc.exit_code) from None
"""


def run_app(script: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script)], env=env, capture_output=True, text=True, check=False)


def load_prompt(path: Path) -> dict:
    return parse.parse_dict(path.read_text(), format=FileFormat.yaml)


def save_prompt(path: Path, doc: dict) -> None:
    file_utils.ensure_parents_write_text(path, dump.dump_as_str(doc, FileFormat.yaml))


with TemporaryDirectory() as tmp:
    cache = Path(tmp) / "cache"
    script = Path(tmp) / "app.py"
    script.write_text(APP_SCRIPT)
    env = os.environ | {
        "CACHE_DIR": str(cache),
        AskShellSettings.ENV_NAME_USE_DEFAULTS: "false",
    }
    settings = AskShellSettings.from_env(CACHE_DIR=str(cache))
    prompt_path = settings.scoped_non_interactive_prompt_path(app_name="demo", command_name="release")

    run1 = run_app(script, env)
    doc = load_prompt(prompt_path)
    print(run1.returncode)
    #> 1
    print(len(doc["questions"]))
    #> 1
    print(doc["questions"][0]["response"])
    #> undecided
    print(doc["session"]["pinned"])
    #> True

    doc["questions"][0]["response"] = True
    save_prompt(prompt_path, doc)
    env = env | {AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH: str(prompt_path)}

    run2 = run_app(script, env)
    doc = load_prompt(prompt_path)
    print(run2.returncode)
    #> 1
    print(len(doc["questions"]))
    #> 2
    print(doc["questions"][0]["response"], doc["questions"][1]["response"])
    #> True undecided

    doc["questions"][1]["response"] = "v1.0"
    save_prompt(prompt_path, doc)

    run3 = run_app(script, env)
    result_line = next(line for line in run3.stdout.splitlines() if line.startswith("shipped="))
    print(run3.returncode)
    #> 0
    print(result_line)
    #> shipped=True name=v1.0
    print(prompt_path.exists())
    #> False
    print(len(list(prompt_path.parent.glob("*non_interactive_prompt.yaml"))))
    #> 1
```
