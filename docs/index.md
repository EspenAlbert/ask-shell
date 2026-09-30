# ask-shell

[![PyPI](https://img.shields.io/pypi/v/ask-shell)](https://pypi.org/project/ask-shell/)
[![GitHub](https://img.shields.io/github/license/EspenAlbert/ask-shell)](https://github.com/EspenAlbert/ask-shell)
[![codecov](https://codecov.io/gh/EspenAlbert/ask-shell/graph/badge.svg)](https://codecov.io/gh/EspenAlbert/ask-shell)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://espenalbert.github.io/ask-shell/)

Python library for CLIs that use interactive prompts, subprocess runs with [Rich](https://rich.readthedocs.io/) output, and test helpers so the same flows run in tests without a TTY.

- **Install**: `uv add ask-shell` or `pip install ask-shell` (Python 3.13+)
- **Docs**: [GitHub Pages](https://espenalbert.github.io/ask-shell/)

## What it provides

- **ask**: Prompts (confirm, text, select list/dict, single and multiple choice) built on [questionary](https://questionary.readthedocs.io/), with Rich styling
- **shell**: Run shell commands via `run`, `run_and_wait`, and `run_pool`; prefixed live output, optional log dirs, retries, and interrupt handling
- **console**: Rich console and progress utilities; `configure_logging(app)` wires a [Typer](https://typer.tiangolo.com/) app to Rich logging (handler, command decorator, optional secret hiding)
- **shell_events**: Callbacks for run lifecycle (before/after, stdout/stderr) for custom handling
- **AskShellSettings**: Paths and options (e.g. run log directory); plug into your config or env

## Non-interactive prompts

When a CLI runs without a TTY, ask-shell does not block on a prompt. It writes the question to a prompt file and exits with `NonInteractivePromptError`, so an agent or CI job can fill in the answer and re-run the same command.

- **Prompt file**: `cache_root/{app}/{command}/non_interactive_prompt.yaml`, one file per command. `CACHE_DIR` (or the platform cache dir) sets `cache_root`.
- **Lock file**: a sibling `.lock` held for the duration of a run. A second run over the same file fails fast with `PromptSessionLockedError` instead of racing.

### Env vars

- **`ASK_SHELL_NON_INTERACTIVE_PROMPT_PATH`**: Pin the prompt file for this run. Point it at a file with earlier answers to replay them.
- **`ASK_SHELL_REPLAY_PROMPT_FILE_IN_TTY`**: In a TTY, replay recorded answers from the file instead of asking again. Opt-in, for resuming after a crash. Non-interactive runs replay without this flag.
- **`ASK_SHELL_SKIP_NON_INTERACTIVE_PROMPT_FILE`**: Skip the prompt file and its lock. Use for a command that never prompts, so a leftover file cannot block it.
- **`ASK_SHELL_USE_DEFAULTS`**: Default true. In a non-interactive run, a prompt with a caller default returns that default instead of dumping the question. Set false to always dump and collect an answer.

### Leftover file after a failure

When a wrapped command fails and a prompt file with questions exists, ask-shell prints a hint. The hint separates the failure from the file: the failure is unrelated to the file, and the file is left over from an earlier run. It then names the actions:

- Delete the file to start over.
- Set `ASK_SHELL_REPLAY_PROMPT_FILE_IN_TTY=true` in a TTY to replay recorded answers.
- Set `ASK_SHELL_SKIP_NON_INTERACTIVE_PROMPT_FILE=true` for a command that never prompts.

Deleting the file is safe when you are not resuming: the next run recreates it. If the failure is unrelated to prompts, fix that failure first. The hint is informational, not the cause.

### Agent and human on the same command

The file is scoped per command, so an agent's run and a human run of the same command share one path.

- The agent leaves recorded answers. A human TTY run asks directly unless they opt in with `ASK_SHELL_REPLAY_PROMPT_FILE_IN_TTY=true`.
- While one run holds the lock, another run over the same file fails fast. Wait for the first run, or delete the file if it is stale.

## Quick example

```python
from ask_shell import ask, shell

if ask.confirm("Run the script?", default=True):
    name = ask.text("Name:", default="world")
    shell.run_and_wait(f"echo Hello, {name}")
```

## Testing

Use `question_patcher` to feed fixed responses to prompts, or `raise_on_question` to fail fast when a prompt is hit. Both are context managers; see the [ask API docs](https://espenalbert.github.io/ask-shell/ask/) for details.

```python
from ask_shell import ask
from ask_shell.ask import question_patcher

with question_patcher(responses=["y", "myname"]):
    assert ask.confirm("Run?")
    assert ask.text("Name:") == "myname"
```

## License

MIT. See [LICENSE](https://github.com/EspenAlbert/ask-shell/blob/main/LICENSE).
