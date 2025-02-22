from textual.app import App
from textual.widgets import Footer, Header, TabbedContent, TabPane

from .pane.newTrade import NewTrade
from .pane.setting import Setting


class ChkTrade(App):
    def compose(self):
        yield Header(show_clock=True)
        with TabbedContent(initial="settingPane"):
            with TabPane("New Trade", id="newTradePane"):
                yield NewTrade()
            with TabPane("Setting", id="settingPane"):
                yield Setting()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "ChkTrade"
        self.sub_title = "A terminal based trade journal"


app = ChkTrade


def main():
    app().run()
