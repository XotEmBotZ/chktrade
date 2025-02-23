from textual import on
from textual.widgets import Static, Placeholder, Select, Switch
from textual.containers import Container, Grid, Horizontal
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
                yield InpContainer()
            with Container():
                yield Placeholder("2")


class InpContainer(Static):
    def compose(self):
        with Container():
            tickerCont = Grid()
            tickerCont.styles.grid_size_columns = 2
            tickerCont.styles.height = "auto"
            with tickerCont:
                yield TextInput(label="Ticker", mapper=lambda x: x.upper())
                yield WidgetWithTitle(
                    Select(options=tuple(map(lambda x: (x, x), ccxt.exchanges))),
                    title="Exchange",
                )
            orderCont = Horizontal()
            orderCont.styles.height = "auto"
            with orderCont:
                dirSwitch = WidgetWithTitle(Switch(False), title="L/S")
                dirSwitch.styles.width = "auto"
                yield dirSwitch
                yield WidgetWithTitle(
                    Select(options=(("Market", "market"), ("Limit", "limit"))),
                    title="Order",
                )
            priceCont = Grid()
            priceCont.styles.grid_size_columns = 4
            priceCont.styles.height = "auto"
            with priceCont:
                yield TextInput(label="Price", classes="priceInp")
                yield TextInput(label="Quantity", classes="priceInp")
                yield TextInput(label="Size", disabled=True, classes="priceInp")
                yield TextInput(label="StopLoss", classes="priceInp")

    @on(TextInput.Changed, ".priceInp")
    def setQuantity(self, event: TextInput.Changed):
        print(event.value)
