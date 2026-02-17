# SelectOptions

<!-- === DO_NOT_EDIT: pkg-ext selectoptions_def === -->
## class: SelectOptions
- [source](../../ask_shell/_internal/interactive.py#L140)
> **Since:** 0.3.0

```python
class SelectOptions(BaseModel):
    use_search_filter: bool | object = <object object>
    use_shortcuts: bool | object = <object object>
    use_jk_keys: bool | object = <object object>
    new_handler_choice: NewHandlerChoice[~T] | None = None
```
<!-- === OK_EDIT: pkg-ext selectoptions_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| use_search_filter | `bool | object` | `<object object>` | 0.3.0 |
| use_shortcuts | `bool | object` | `<object object>` | 0.3.0 |
| use_jk_keys | `bool | object` | `<object object>` | 0.3.0 |
| new_handler_choice | `NewHandlerChoice[~T] | None` | `None` | unreleased |

<!-- === DO_NOT_EDIT: pkg-ext selectoptions_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'new_handler_choice' default added: None |
| unreleased | added base class 'BaseModel' |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext selectoptions_changes === -->