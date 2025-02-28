from textual import on
from textual.widgets import Static, Placeholder, Select, Switch, Input
from textual.containers import Container, Grid, Horizontal, VerticalScroll, ItemGrid
from textual.validation import Function
import ccxt

from ..utils.models import AppConfig

from ..utils.widget import TextInput, WidgetWithTitle, radioSetCreator, switchCreator


class NewTrade(Static):
    def __init__(self, appConfig: AppConfig):
        self.appConfig: AppConfig = appConfig
        super().__init__()

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
        self.gridWidget.styles.grid_gutter_horizontal = 1
        self.gridWidget.styles.grid_gutter_vertical = 1
        with self.gridWidget:
            self.inpCont = Container(id="newTradeInpCont")
            with self.inpCont:
                yield InpContainer(appConfig=self.appConfig)
            with Container():
                yield Placeholder("2")


class InpContainer(Static):
    def __init__(self, appConfig: AppConfig):
        self.appConfig: AppConfig = appConfig
        super().__init__()

    def compose(self):
        with VerticalScroll():
            with WidgetWithTitle(title="Order Details"):
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
            with WidgetWithTitle(title="Procedure"):
                grid = Container()
                with grid:
                    for (
                        custInpId,
                        custInpVal,
                    ) in self.appConfig.newTradeConfig.customInputs.items():
                        if custInpVal.type == "option" and custInpVal.options:
                            yield radioSetCreator(
                                title=custInpVal.title.capitalize(),
                                options=custInpVal.options,
                                id=custInpId,
                            )
                        elif custInpVal.type == "bool":
                            yield switchCreator(custInpVal.title, id=custInpId)

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
