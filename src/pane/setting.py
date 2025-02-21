import os
import yaml
import dotenv
from textual.validation import Function
from textual.widgets import Label, Static, Button, Input
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
        yield Button("Save", id="settingBtnSave", action="save_config")
        yield Button("Reset", id="settingBtnReset", action="reset_config")

    def action_save_config(self):
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

    async def action_reset_config(self):
        await self.recompose()
