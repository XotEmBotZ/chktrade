from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


class CustomInputs(BaseModel):
    class CustomOptionsInput(BaseModel):
        class CustomOption(BaseModel):
            title: str
            timeout: int = 0
            popup: Optional[str] = None

        title: str
        options: dict[str, CustomOption]

    class CustomBoolsInput(BaseModel):
        title: str
        timeout: int = 0
        popup: Optional[str] = None

    options: Optional[dict[str, CustomOptionsInput]]
    bools: Optional[dict[str, CustomBoolsInput]]

    @model_validator(mode="after")
    def validate_model(self):
        idList = []
        if self.options:
            idList.extend(self.options.keys())
        if self.bools:
            idList.extend(self.bools.keys())
        if len(set(idList)) != len(idList):
            raise ValueError("All IDs must be same")
        return self


class NewTradeConfig(BaseModel):
    customInputs: CustomInputs = Field(alias="custom_inputs")
    checklist: list[str] = Field(alias="checklist")


class AppConfig(BaseModel):
    newTradeConfig: NewTradeConfig = Field(alias="new_trade")


if __name__ == "__main__":
    import yaml
    from pprint import pprint

    pprint(
        yaml.safe_load(
            open("config/config.yaml"),
        )
    )

    a = AppConfig(
        **yaml.safe_load(
            open("config/config.yaml"),
        )
    )
