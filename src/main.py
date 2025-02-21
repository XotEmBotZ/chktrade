from textual.app import App
from textual.widgets import Header, Footer, TabbedContent, TabPane, Placeholder
from .pane.setting import Setting


class ChkTrade(App):
    def compose(self):
        yield Header(show_clock=True)
        with TabbedContent(initial="settingPane"):
            with TabPane("New Trade", id="newTradePane"):
                yield Placeholder("new trade")
            with TabPane("Setting", id="settingPane"):
                yield Setting()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "ChkTrade"
        self.sub_title = "A terminal based trade journal"


app = ChkTrade
