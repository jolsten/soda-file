import datetime
from typing import Literal
from typing_extensions import Annotated
from pydantic import BeforeValidator, PlainSerializer


def validate_yymmdd(yymmdd: str) -> datetime.date:
    dt = datetime.datetime.strptime(yymmdd, "%y%m%d")
    return dt.date()


def validate_hhmmss(hhmmss: str) -> datetime.time:
    hh, mm, ss = int(hhmmss[0:2]), int(hhmmss[2:4]), int(hhmmss[4:6])
    return datetime.time(hh % 24, mm % 60, ss % 60)


def to_upper(value: str) -> str:
    return value.upper()


def to_yymmdd(date: datetime.date) -> str:
    return date.strftime("%y%M%D")


def to_hhmmss(time: datetime.time) -> str:
    return time.strftime("%H%M%S")


YYMMDD = Annotated[
    datetime.date,
    BeforeValidator(validate_yymmdd),
    PlainSerializer(to_yymmdd, return_type=str),
]

HHMMSS = Annotated[
    datetime.time,
    BeforeValidator(validate_hhmmss),
    PlainSerializer(to_hhmmss, return_type=str),
]

ByteOrder = Annotated[
    Literal["MSBF", "LSBF"],
    BeforeValidator(to_upper),
    PlainSerializer(to_upper),
]
