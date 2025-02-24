from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


class Options(BaseModel):
    title: str
    timeout: int = 0


class NewTradeCustomInputs(BaseModel):
    title: str
    type: Literal["option"] | Literal["bool"]
    timeout: int = 0
    options: Optional[list] = None

    @model_validator(mode="after")
    def validate_timeout(self):
        if self.type == "option":
            if self.timeout:
                raise ValueError(
                    "Timeout is not supported globally for option type. Kindly use timeout in individual options"
                )
            if not self.options or len(self.options) == 0:
                raise ValueError("No options were given.")
        return self


class NewTradeConfig(BaseModel):
    customInputs: list[NewTradeCustomInputs] = Field(alias="custom_inputs")
    checklist: list[str] = Field(alias="checklist")


class AppConfig(BaseModel):
    newTradeConfig: NewTradeConfig = Field(alias="new_trade")


if __name__ == "__main__":
    from pprint import pprint
    import yaml

    pprint(
        AppConfig(
            **yaml.safe_load(
                open("config/config.yaml"),
            )
        ).model_dump_json()
    )
