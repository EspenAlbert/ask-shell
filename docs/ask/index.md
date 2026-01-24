<!-- === DO_NOT_EDIT: pkg-ext header === -->
# ask

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`ChoiceTyped`](#choicetyped_def)
- [`KeyInput`](#keyinput_def)
- [`NewHandlerChoice`](#newhandlerchoice_def)
- [`PromptMatch`](#promptmatch_def)
- [`RaiseOnQuestionError`](#raiseonquestionerror_def)
- [`SelectOptions`](#selectoptions_def)
- [`confirm`](#confirm_def)
- [`force_interactive`](#force_interactive_def)
- [`question_patcher`](#question_patcher_def)
- [`raise_on_question`](#raise_on_question_def)
- [`select_dict`](#select_dict_def)
- [`select_list`](#select_list_def)
- [`select_list_choice`](#select_list_choice_def)
- [`select_list_multiple`](#select_list_multiple_def)
- [`select_list_multiple_choices`](#select_list_multiple_choices_def)
- [`text`](#text_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext choicetyped_def === -->
<a id="choicetyped_def"></a>

### class: `ChoiceTyped`
- [source](../../ask_shell/_internal/interactive.py#L106)
> **Since:** 0.3.0

```python
class ChoiceTyped(Generic):
    name: str
    value: ~T
    description: str | None = None
    checked: bool = False
```

| Field | Type | Default | Since |
|---|---|---|---|
| name | `str` | - | 0.3.0 |
| value | `~T` | - | 0.3.0 |
| description | `str | None` | `None` | 0.3.0 |
| checked | `bool` | `False` | 0.3.0 |
<!-- === OK_EDIT: pkg-ext choicetyped_def === -->
<!-- === DO_NOT_EDIT: pkg-ext keyinput_def === -->
<a id="keyinput_def"></a>

### class: `KeyInput`
- [source](../../ask_shell/_internal/interactive.py#L316)
> **Since:** 0.3.0

```python
class KeyInput:
    ...
```
<!-- === OK_EDIT: pkg-ext keyinput_def === -->
<!-- === DO_NOT_EDIT: pkg-ext newhandlerchoice_def === -->
<a id="newhandlerchoice_def"></a>

### class: `NewHandlerChoice`
- [source](../../ask_shell/_internal/interactive.py#L100)
> **Since:** 0.3.0

```python
class NewHandlerChoice(Generic):
    constructor: Callable[[<class 'str'>], ~T]
    new_prompt: str
```

| Field | Type | Default | Since |
|---|---|---|---|
| constructor | `Callable[[<class 'str'>], ~T]` | - | 0.3.0 |
| new_prompt | `str` | - | 0.3.0 |
<!-- === OK_EDIT: pkg-ext newhandlerchoice_def === -->
<!-- === DO_NOT_EDIT: pkg-ext promptmatch_def === -->
<a id="promptmatch_def"></a>

### class: `PromptMatch`
- [source](../../ask_shell/_internal/interactive.py#L338)
> **Since:** 0.3.0

```python
class PromptMatch:
    response: str | None = None
    responses: list[str] = ...
    substring: str = ''
    exact: str = ''
    max_matches: int = 1
    matches_so_far: int = 0
```

| Field | Type | Default | Since |
|---|---|---|---|
| response | `str | None` | `None` | 0.3.0 |
| responses | `list[str]` | `...` | 0.3.0 |
| substring | `str` | `''` | 0.3.0 |
| exact | `str` | `''` | 0.3.0 |
| max_matches | `int` | `1` | 0.3.0 |
| matches_so_far | `int` | `0` | 0.3.0 |
<!-- === OK_EDIT: pkg-ext promptmatch_def === -->
<!-- === DO_NOT_EDIT: pkg-ext raiseonquestionerror_def === -->
<a id="raiseonquestionerror_def"></a>

### exception: `RaiseOnQuestionError`
- [source](../../ask_shell/_internal/interactive.py#L504)
> **Since:** 0.3.0

```python
class RaiseOnQuestionError(Exception):
    ...
```
<!-- === OK_EDIT: pkg-ext raiseonquestionerror_def === -->
<!-- === DO_NOT_EDIT: pkg-ext selectoptions_def === -->
<a id="selectoptions_def"></a>

### class: `SelectOptions`
- [source](../../ask_shell/_internal/interactive.py#L140)
> **Since:** 0.3.0

```python
class SelectOptions(BaseModel, Generic):
    use_search_filter: bool | object = <object object>
    use_shortcuts: bool | object = <object object>
    use_jk_keys: bool | object = <object object>
    new_handler_choice: NewHandlerChoice[~T] | None
```

| Field | Type | Default | Since |
|---|---|---|---|
| use_search_filter | `bool | object` | `<object object>` | 0.3.0 |
| use_shortcuts | `bool | object` | `<object object>` | 0.3.0 |
| use_jk_keys | `bool | object` | `<object object>` | 0.3.0 |
| new_handler_choice | `NewHandlerChoice[~T] | None` | - | 0.3.0 |
<!-- === OK_EDIT: pkg-ext selectoptions_def === -->
<!-- === DO_NOT_EDIT: pkg-ext confirm_def === -->
<a id="confirm_def"></a>

### function: `confirm`
- [source](../../ask_shell/_internal/interactive.py#L81)
> **Since:** 0.3.0

```python
def confirm(prompt_text: str, *, default: bool | None = None) -> bool:
    ...
```
<!-- === OK_EDIT: pkg-ext confirm_def === -->
<!-- === DO_NOT_EDIT: pkg-ext force_interactive_def === -->
<a id="force_interactive_def"></a>

### class: `force_interactive`
- [source](../../ask_shell/_internal/interactive.py#L381)
> **Since:** 0.3.0

```python
class force_interactive:
    settings: AskShellSettings = ...
```

| Field | Type | Default | Since |
|---|---|---|---|
| settings | `AskShellSettings` | `...` | 0.3.0 |
<!-- === OK_EDIT: pkg-ext force_interactive_def === -->
<!-- === DO_NOT_EDIT: pkg-ext question_patcher_def === -->
<a id="question_patcher_def"></a>

### class: `question_patcher`
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

| Field | Type | Default | Since |
|---|---|---|---|
| settings | `AskShellSettings` | `...` | 0.3.0 |
| responses | `list[str]` | `...` | 0.3.0 |
| next_response | `int` | `0` | 0.3.0 |
| dynamic_responses | `list[PromptMatch]` | `...` | 0.3.0 |
<!-- === OK_EDIT: pkg-ext question_patcher_def === -->
<!-- === DO_NOT_EDIT: pkg-ext raise_on_question_def === -->
<a id="raise_on_question_def"></a>

### class: `raise_on_question`
- [source](../../ask_shell/_internal/interactive.py#L510)
> **Since:** 0.3.0

```python
class raise_on_question(force_interactive):
    settings: AskShellSettings = ...
    raise_error: Callable[[<class 'str'>], BaseException] = <class 'ask_shell._internal.interactive.RaiseOnQuestionError'>
```

| Field | Type | Default | Since |
|---|---|---|---|
| settings | `AskShellSettings` | `...` | 0.3.0 |
| raise_error | `Callable[[<class 'str'>], BaseException]` | `<class 'ask_shell._internal.interactive.RaiseOnQuestionError'>` | 0.3.0 |
<!-- === OK_EDIT: pkg-ext raise_on_question_def === -->
<!-- === DO_NOT_EDIT: pkg-ext select_dict_def === -->
<a id="select_dict_def"></a>

### function: `select_dict`
- [source](../../ask_shell/_internal/interactive.py#L261)
> **Since:** 0.3.0

```python
def select_dict(prompt_text: str, choices: dict[str, ~T], *, default: str | None = None, options: SelectOptions | None = None) -> ~T:
    ...
```
<!-- === OK_EDIT: pkg-ext select_dict_def === -->
<!-- === DO_NOT_EDIT: pkg-ext select_list_def === -->
<a id="select_list_def"></a>

### function: `select_list`
- [source](../../ask_shell/_internal/interactive.py#L277)
> **Since:** 0.3.0

```python
def select_list(prompt_text: str, choices: list[str], *, default: str | None = None, options: SelectOptions | None = None) -> str:
    ...
```
<!-- === OK_EDIT: pkg-ext select_list_def === -->
<!-- === DO_NOT_EDIT: pkg-ext select_list_choice_def === -->
<a id="select_list_choice_def"></a>

### function: `select_list_choice`
- [source](../../ask_shell/_internal/interactive.py#L302)
> **Since:** 0.3.0

```python
def select_list_choice(prompt_text: str, choices: list[ChoiceTyped[~T]], *, default: ~T | None = None, options: SelectOptions | None = None) -> ~T:
    ...
```
<!-- === OK_EDIT: pkg-ext select_list_choice_def === -->
<!-- === DO_NOT_EDIT: pkg-ext select_list_multiple_def === -->
<a id="select_list_multiple_def"></a>

### function: `select_list_multiple`
- [source](../../ask_shell/_internal/interactive.py#L230)
> **Since:** 0.3.0

```python
def select_list_multiple(prompt_text: str, choices: list[str], *, default: list[str] | None = None, options: SelectOptions | None = None) -> list[str]:
    ...
```
<!-- === OK_EDIT: pkg-ext select_list_multiple_def === -->
<!-- === DO_NOT_EDIT: pkg-ext select_list_multiple_choices_def === -->
<a id="select_list_multiple_choices_def"></a>

### function: `select_list_multiple_choices`
- [source](../../ask_shell/_internal/interactive.py#L246)
> **Since:** 0.3.0

```python
def select_list_multiple_choices(prompt_text: str, choices: list[ChoiceTyped[~T]], default: list[~T] | None = None, *, options: SelectOptions | None = None) -> list[~T]:
    ...
```
<!-- === OK_EDIT: pkg-ext select_list_multiple_choices_def === -->
<!-- === DO_NOT_EDIT: pkg-ext text_def === -->
<a id="text_def"></a>

### function: `text`
- [source](../../ask_shell/_internal/interactive.py#L129)
> **Since:** 0.3.0

```python
def text(prompt_text: str, default: str = '') -> str:
    ...
```
<!-- === OK_EDIT: pkg-ext text_def === -->