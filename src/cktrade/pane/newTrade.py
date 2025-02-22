from textual.widgets import Static, TextArea, Input, Placeholder, Button, Select
from textual.containers import Container, Grid, Horizontal
from textual import on
from textual.reactive import reactive
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
            with tickerCont:
                yield TextInput(lable="Ticker")
                yield WidgetWithTitle(
                    Select(options=tuple(map(lambda x: (x, x), ccxt.exchanges))),
                    title="Exchange",
                )
