from typing import Iterable
from collections.abc import Callable

from rich.console import RenderableType
from rich.highlighter import Highlighter
from textual import on
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.suggester import Suggester
from textual.validation import Validator
from textual.widgets import Button, Input, Label, Static
from textual.widgets._input import InputType, InputValidationOn
from textual.widget import Widget
from textual.app import ComposeResult
from textual.screen import ModalScreen


class TextInput(Static):
    BINDINGS = [
        Binding("escape", "escape", "Escape"),
    ]

    class Changed(Input.Changed): ...

    class Submitted(Input.Submitted): ...

    def __init__(
        self,
        value: str | None = None,
        placeholder: str = "",
        highlighter: Highlighter | None = None,
        password: bool = False,
        label: str | None = None,
        restrict: str | None = None,
        type: InputType = "text",  # type: ignore
        max_length: int = 0,
        suggester: Suggester | None = None,
        validators: Validator | Iterable[Validator] | None = None,
        validate_on: Iterable[InputValidationOn] | None = None,
        valid_empty: bool = False,
        select_on_focus: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        tooltip: RenderableType | None = None,
        mapper: Callable[[str], str] | None = None,
    ):
        super().__init__()
        self.cust_value = value
        self.cust_placeholder = placeholder
        self.cust_highlighter = highlighter
        self.cust_password = password
        self.cust_lable = label
        self.cust_restrict = restrict
        self.cust_type = type
        self.cust_max_length = max_length
        self.cust_suggester = suggester
        self.cust_validators = validators
        self.cust_validate_on = validate_on
        self.cust_valid_empty = valid_empty
        self.cust_select_on_focus = select_on_focus
        self.cust_name = name  # type: ignore
        self.cust_id = id  # type: ignore
        self.cust_classes = classes
        self.cust_disabled = disabled
        self.cust_tooltip = tooltip
        self.mapper = mapper

    DEFAULT_CSS = """
        .TextInputClass {
            height: auto;
            border: solid $secondary;
            border-title-align: left;
        }
        """
    value: str = ""

    def compose(self):
        self.container = Container(
            id="cont_" + self.cust_id if self.cust_id else None,
            name="cont_" + self.cust_name if self.cust_name else None,
            classes=self.cust_classes + " TextInputClass"
            if self.cust_classes
            else " TextInputClass",
            disabled=self.cust_disabled,
        )
        self.container.border_title = self.cust_lable
        self.inp = Input(
            value=self.cust_value,
            placeholder=self.cust_placeholder,
            highlighter=self.cust_highlighter,
            password=self.cust_password,
            restrict=self.cust_restrict,
            type=self.cust_type,  # type: ignore
            max_length=self.cust_max_length,
            suggester=self.cust_suggester,
            validators=self.cust_validators,
            validate_on=self.cust_validate_on,
            valid_empty=self.cust_valid_empty,
            select_on_focus=self.cust_select_on_focus,
            name=self.cust_name,
            id=self.cust_id,
            classes=self.cust_classes,
            disabled=self.cust_disabled,
            tooltip=self.cust_tooltip,
        )
        self.validation = Container()
        self.validation.styles.height = "auto"
        self.validation.styles.margin = (0, 0, 0, 2)
        with self.container:
            yield self.inp
            yield self.validation

    @on(Input.Changed)
    def setValue(self, event: Input.Changed):
        if self.mapper:
            self.inp.value = self.mapper(event.value)
        self.value = self.inp.value

    @on(Input.Changed)
    def show_error(self, event: Input.Changed):
        self.validation.remove_children()
        if not event.validation_result:
            return
        if not event.validation_result.is_valid:
            for desc in event.validation_result.failure_descriptions:
                txt = Label(desc)
                self.validation.mount(txt)

    def action_escape(self) -> None:
        self.app.set_focus(self.app.query_one(Button))


class WidgetWithTitle(Container):
    DEFAULT_CSS = """
        WidgetWithTitle {
            height: auto;
            border: solid $secondary;
            border-title-align: left;
            # width: auto;
        }
    """

    def __init__(self, widget: Widget, title: str) -> None:
        super().__init__()
        self._widget = widget
        self.border_title = title

    def compose(self) -> ComposeResult:
        yield self._widget


class TextPopup(ModalScreen):
    def __init__(self, text: str, timeout: int, *args, **kwargs):
        self.text = text
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.set_timer(self.timeout, self.enableBtn)
        self.styles.align = ("center", "middle")

    def compose(self) -> ComposeResult:
        container = Vertical()
        container.styles.height = "auto"
        container.styles.width = "auto"
        container.styles.padding = (1, 5)
        container.styles.background = self.app.theme_variables["surface"]
        with container:
            yield Label(self.text)
            yield Button("Understood!", disabled=True, variant="error")

    def enableBtn(self):
        self.query_exactly_one(Button).disabled = False
        self.set_focus(self.query_exactly_one(Button))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
