from textual import on
from textual.widgets import Static, Placeholder, Select, Switch, Input
from textual.containers import Container, Grid, Horizontal
from textual.validation import Function
import ccxt

from ..utils.widget import TextInput, WidgetWithTitle


class NewTrade(Static):
    def on_mount(self):
        print(self.app.size)

    def on_resize(self):
        self.gridWidget.styles.layout = (
            "horizontal"
            if int(self.app.size.width / 2) > self.app.size.height * 1.5
            else "vertical"
        )

    def compose(self):
        self.gridWidget = Grid(id="newTradeGrid")
        with self.gridWidget:
            self.inpCont = Container(id="newTradeInpCont")
            with self.inpCont:
                yield WidgetWithTitle(InpContainer(), title="Order Details")
            with Container():
                yield Placeholder("2")


class InpContainer(Static):
    def compose(self):
        with Container():
            tickerCont = Grid()
            tickerCont.styles.grid_size_columns = 2
            tickerCont.styles.height = "auto"
            with tickerCont:
                yield TextInput(
                    label="Ticker",
                    mapper=lambda x: x.upper(),
                    validators=(
                        Function(lambda x: bool(x), "Empty Value not allowed"),
                    ),
                    id="tickerInp",
                )
                yield WidgetWithTitle(
                    Select(
                        options=tuple(map(lambda x: (x, x), ccxt.exchanges)),
                        allow_blank=False,
                        id="exchageInp",
                    ),
                    title="Exchange",
                )
            orderCont = Horizontal()
            orderCont.styles.height = "auto"
            with orderCont:
                dirSwitch = WidgetWithTitle(Switch(True), title="S/L")
                dirSwitch.styles.width = "auto"
                yield dirSwitch
                yield WidgetWithTitle(
                    Select(
                        options=(("Market", "market"), ("Limit", "limit")),
                        allow_blank=False,
                        id="orderTypeInp",
                    ),
                    title="Order",
                )
            priceCont = Grid()
            priceCont.styles.grid_size_columns = 4
            priceCont.styles.height = "auto"
            with priceCont:
                yield TextInput(
                    label="Price",
                    type="number",
                    classes="priceInp",
                    id="priceInp",
                )
                yield TextInput(
                    label="Quantity",
                    type="number",
                    classes="priceInp",
                    id="priceQtyInp",
                )
                yield TextInput(
                    label="Size",
                    disabled=True,
                    type="number",
                    classes="priceInp",
                    id="priceSizeInp",
                )
                yield TextInput(
                    label="StopLoss",
                    type="number",
                    classes="priceInp",
                    id="priceSLInp",
                )

    @on(Input.Changed, ".priceInp")
    def setQuantity(self, event: TextInput.Changed):
        if (
            self.query_exactly_one("#priceInp", Input).is_valid
            and self.query_exactly_one("#priceQtyInp", Input).is_valid
            and self.query_exactly_one("#priceInp", Input).value
            and self.query_exactly_one("#priceQtyInp", Input).value
        ):
            self.query_exactly_one("#priceSizeInp", Input).value = str(
                float(self.query_exactly_one("#priceInp", Input).value)
                * float(self.query_exactly_one("#priceQtyInp", Input).value)
            )
