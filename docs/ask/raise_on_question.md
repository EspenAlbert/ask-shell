# raise_on_question

<!-- === DO_NOT_EDIT: pkg-ext raise_on_question_def === -->
## class: raise_on_question
- [source](../../ask_shell/_internal/interactive.py#L510)
> **Since:** 0.3.0

```python
class raise_on_question(force_interactive):
    settings: AskShellSettings = ...
    raise_error: Callable[[<class 'str'>], BaseException] = <class 'ask_shell._internal.interactive.RaiseOnQuestionError'>
```
<!-- === OK_EDIT: pkg-ext raise_on_question_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| settings | `AskShellSettings` | `...` | 0.3.0 |
| raise_error | `Callable[[<class 'str'>], BaseException]` | `<class 'ask_shell._internal.interactive.RaiseOnQuestionError'>` | 0.3.0 |

<!-- === DO_NOT_EDIT: pkg-ext raise_on_question_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | added base class 'force_interactive' |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext raise_on_question_changes === -->