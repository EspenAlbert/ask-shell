# question_patcher

<!-- === DO_NOT_EDIT: pkg-ext question_patcher_def === -->
## class: question_patcher
- [source](../../ask_shell/_internal/interactive.py#L397)
> **Since:** 0.3.0

```python
class question_patcher(force_interactive):
    settings: AskShellSettings = ...
    responses: list[str] = ...
    next_response: int = 0
    dynamic_responses: list[PromptMatch] = ...
```

Context manager to patch the questionary.ask_question, useful for testing.

Uses PlainTextOutput with a controlled buffer and direct unsafe_ask() calls
to avoid I/O conflicts with Click's CliRunner. The CliRunner replaces
sys.stdout/stderr with its own wrappers, and if we use DummyOutput or
thread pools, prompt_toolkit may still write to closed streams.
<!-- === OK_EDIT: pkg-ext question_patcher_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| settings | `AskShellSettings` | `...` | 0.3.0 |
| responses | `list[str]` | `...` | 0.3.0 |
| next_response | `int` | `0` | 0.3.0 |
| dynamic_responses | `list[PromptMatch]` | `...` | 0.3.0 |

<!-- === DO_NOT_EDIT: pkg-ext question_patcher_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | added base class 'force_interactive' |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext question_patcher_changes === -->