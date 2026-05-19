from pathlib import Path

import pytest
from pytest_examples import CodeExample, EvalExample, find_examples

PACKAGE_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = PACKAGE_ROOT / "docs" / "examples"


@pytest.fixture(autouse=True)
def _examples_package_cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(PACKAGE_ROOT)


@pytest.mark.parametrize("example", find_examples(EXAMPLES_DIR), ids=str)
def test_examples(example: CodeExample, eval_example: EvalExample):
    eval_example.set_config(line_length=120, target_version="py313", ruff_ignore=["T"])  # pyright: ignore[reportArgumentType]
    prefix = example.prefix_settings()
    if prefix.get("test", "").startswith("skip"):
        pytest.skip(prefix["test"])
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(example)
    else:
        eval_example.lint(example)
        eval_example.run_print_check(example)
