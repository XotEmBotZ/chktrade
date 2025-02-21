from textual.app import App
from textual.widgets import Header, Footer


class ChkTrade(App):
    def compose(self):
        yield Header()
        yield Footer()


app = ChkTrade
