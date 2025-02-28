from textual.app import App
from textual.widgets import Footer, Header, TabbedContent, TabPane
import yaml
from textual.reactive import reactive
from textual import on

from .pane.newTrade import NewTrade
from .pane.setting import Setting
from .utils.models import AppConfig

from dotenv import load_dotenv


class ChkTrade(App):
    config: reactive[dict] = reactive({})
    appConfig: reactive[AppConfig]

    def compose(self):
        yield Header(show_clock=True)
        with TabbedContent(initial="newTradePane"):
            with TabPane("New Trade", id="newTradePane"):
                yield NewTrade(appConfig=self.appConfig)
            with TabPane("Setting", id="settingPane"):
                yield Setting()
        yield Footer()

    def load_config(self):
        with open(".config.yaml") as f:
            self.config = yaml.safe_load(f)

    def on_load(self):
        self.load_config()

    def on_mount(self) -> None:
        self.title = "ChkTrade"
        self.sub_title = "A terminal based trade journal"

    def watch_config(self, oldConfig, newConfig):
        if len(newConfig) == 0:
            return
        self.appConfig = AppConfig(**yaml.safe_load(open(newConfig["configFilePath"])))
        load_dotenv(newConfig["envFilePath"])

    @on(Setting.Changed)
    def updateConfig(self, event: Setting.Changed):
        self.load_config()


app = ChkTrade


def main():
    app().run()
