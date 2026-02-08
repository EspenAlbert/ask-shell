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
- **console**: Rich console and progress utilities
- **shell_events**: Callbacks for run lifecycle (before/after, stdout/stderr) for custom handling
- **AskShellSettings**: Paths and options (e.g. run log directory); plug into your config or env

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

MIT. See [LICENSE](LICENSE).
