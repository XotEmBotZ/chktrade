import os

import dotenv
import yaml
from textual import on
from textual.containers import Horizontal
from textual.validation import Function
from textual.widgets import Button, Input, Static

from ..utils.widget import TextInput


def isFile(path: str) -> bool:
    return os.path.isfile(path)


def isValidYaml(path: str) -> bool:
    try:
        yaml.load(open(path, "rt"), Loader=yaml.SafeLoader)
        return True
    except yaml.YAMLError:
        return False
    except FileNotFoundError:
        return False


def isValidEnv(path: str):
    return os.path.isfile(path) and bool(dotenv.dotenv_values(path))


class Setting(Static):
    def compose(self):
        try:
            with open("./config/yaml", "rt") as f:
                config = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            config = {
                "configFilePath": "./config/config.yaml",
                "envFilePath": "./config/.env",
            }
        self.configPath = TextInput(
            config["configFilePath"],
            lable="Config Gile",
            validators=[
                Function(isFile, "File is not present"),
                Function(isValidYaml, "Not a valid yaml file"),
            ],
            id="settingConfigInp",
        )
        yield self.configPath
        self.envPath = TextInput(
            config["envFilePath"],
            lable="ENV File",
            validators=[
                Function(isFile, "File is not present"),
                Function(isValidEnv, "Not a valid env file"),
            ],
            id="settingEnvInp",
        )
        yield self.envPath
        horizontalCont = Horizontal()
        horizontalCont.styles.align_horizontal = "center"
        with horizontalCont:
            yield Button("Save", id="settingBtnSave", variant="success")
            yield Button("Reset", id="settingBtnReset", variant="error")

    @on(Button.Pressed, "#settingBtnSave")
    def action_save_config(self, event: Button.Pressed):
        print("ahhaha")
        for inp in self.query(Input):
            if not inp.is_valid:
                break
        else:
            with open("./.config.yaml", "wt") as f:
                yaml.dump(
                    {
                        "configFilePath": self.configPath.value,
                        "envFilePath": self.envPath.value,
                    },
                    stream=f,
                    Dumper=yaml.SafeDumper,
                )
            self.notify(
                message="Configuration Saved",
                title="Success",
                timeout=2,
            )

    @on(Button.Pressed, "#settingBtnReset")
    async def action_reset_config(self, event: Button.Pressed):
        await self.recompose()  # type: ignore
