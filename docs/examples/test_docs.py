from pathlib import Path

import pytest
from pytest_examples import CodeExample, EvalExample, find_examples

EXAMPLES_DIR = Path(__file__).parent


@pytest.mark.parametrize("example", find_examples(str(EXAMPLES_DIR)), ids=str)
def test_examples(example: CodeExample, eval_example: EvalExample):
    eval_example.run_print_check(example)
