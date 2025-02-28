import os

import dotenv
import yaml
from textual import on
from textual.containers import ItemGrid
from textual.validation import Function
from textual.widgets import Button, Input, Static
from textual.message import Message

from ..utils.widget import TextInput
from ..utils.config import dirs


def isFile(path: str) -> bool:
    return os.path.isfile(path)


def isValidYaml(path: str) -> bool:
    if not isFile(path):
        return False
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
    class Changed(Message): ...

    def compose(self):
        config: dict[str, str] = {
            "configFilePath": str(dirs.user_config_path / "config.yaml"),
            "envFilePath": str(dirs.user_config_path / ".env"),
            "dataFilePath": str(dirs.user_data_path / "data.sqlite"),
        }
        try:
            with open(".config.yaml", "rt") as f:
                c = yaml.load(f, Loader=yaml.SafeLoader)
                print(c)
                config.update(c)
                print(config)
        except FileNotFoundError:
            self.notify("App Config not Found Using default values")

        self.configPath = TextInput(
            config["configFilePath"],
            label="Config Gile",
            validators=[
                Function(isFile, "File is not present"),
                Function(isValidYaml, "Not a valid yaml file"),
            ],
            id="settingConfigInp",
        )
        yield self.configPath
        self.envPath = TextInput(
            config["envFilePath"],
            label="ENV File",
            validators=[
                Function(isFile, "File is not present"),
                Function(isValidEnv, "Not a valid env file"),
            ],
            id="settingEnvInp",
        )
        yield self.envPath
        self.dataPath = TextInput(
            config["dataFilePath"],
            label="Data File",
            id="settingDataInp",
        )
        yield self.dataPath

        horizontalCont = ItemGrid(regular=True, min_column_width=1)
        horizontalCont.styles.align_horizontal = "center"
        with horizontalCont:
            yield Button("Create File", id="settingBtnCreate", variant="primary")
            yield Button("Save", id="settingBtnSave", variant="success")
            yield Button("Reset", id="settingBtnReset", variant="error")

    def config_changed(self):
        self.post_message(self.Changed())

    @on(Button.Pressed, "#settingBtnSave")
    def action_save_config(self, event: Button.Pressed):
        for inp in self.query(Input):
            if not inp.is_valid:
                break
        else:
            with open("./.config.yaml", "wt") as f:
                yaml.dump(
                    {
                        "configFilePath": self.configPath.value,
                        "envFilePath": self.envPath.value,
                        "dataFilePath": self.dataPath.value,
                    },
                    stream=f,
                    Dumper=yaml.SafeDumper,
                )
            self.notify(
                message="Configuration Saved",
                title="Success",
                timeout=2,
            )
            self.config_changed()

    @on(Button.Pressed, "#settingBtnReset")
    async def action_reset_config(self, event: Button.Pressed):
        await self.recompose()  # type: ignore

    @on(Button.Pressed, "#settingBtnCreate")
    def action_create_file(self, event: Button.Pressed):
        open(self.configPath.value, "wt")
        open(self.envPath.value, "wt")
        open(self.dataPath.value, "wb")
