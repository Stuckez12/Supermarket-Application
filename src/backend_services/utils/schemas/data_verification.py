from datetime import datetime
from pydantic import BaseModel, Field
from typing import Type, Union

from utils.enums import TriBool


class StringConfig(BaseModel):
    min_len: int = 2
    max_len: int = 64
    include_lowercase: TriBool = TriBool.TRUE
    include_uppercase: TriBool = TriBool.NONE
    include_number: TriBool = TriBool.NONE
    include_specials: TriBool = TriBool.FALSE


class NumberConfig(BaseModel):
    number_type: Type[int | float] = int
    min_val: int = 0
    max_val: int = 100


class DateTimeConfig(BaseModel):
    min_datetime: datetime = Field(default_factory=datetime.now)
    max_datetime: datetime = Field(default_factory=datetime.now)


DataTypeConfig = Union[DateTimeConfig, NumberConfig, StringConfig]
