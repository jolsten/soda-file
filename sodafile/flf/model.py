import pathlib
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator

from sodafile.flf.reader import FLFReader
from .typing import YYMMDD, HHMMSS, ByteOrder, Frequency
from .utils import dict_upper, dict_lower


class SectionBase(BaseModel):
    model_config = ConfigDict(extra="allow")


class Volume(SectionBase):
    creation: YYMMDD
    classification: str
    byte: Optional[ByteOrder] = None


class File(SectionBase):
    creation: YYMMDD
    classification: str
    byte: Optional[ByteOrder] = None
    block: int
    rbpl: int
    rbrp: int


class Event(SectionBase):
    date: YYMMDD
    vehicle: str
    sput: Optional[str] = None


class Signal(SectionBase):
    uptime: HHMMSS
    downtime: HHMMSS
    designator: str
    frequency: Frequency


class Input(SectionBase):
    pass


class Selector(SectionBase):
    number: int


class Processor(SectionBase):
    channels: int
    rate: float


class Record(SectionBase):
    word: int
    rrln: int
    rrpl: int
    rdpl: int
    rdid: int
    rdes: int
    rdst: int
    rdin: int
    auxiliary: str


class Output(SectionBase):
    pass


class FLF(SectionBase):
    volume: Optional[Volume] = None
    file: File
    event: Event
    signal: Signal
    input: Input
    selector: Selector
    processor: Processor
    record: Record
    output: Output
    comments: Optional[str] = None

    @property
    def byte_order(self) -> ByteOrder:
        if self.volume and self.volume.byte:
            return self.volume.byte
        if self.file and self.file.byte:
            return self.file.byte
        return "MSBF"

    @classmethod
    def from_text(cls, text: str) -> "FLF":
        reader = FLFReader.from_text(text)
        return cls(**dict_lower(reader.data))

    @classmethod
    def from_file(cls, file: str) -> "FLF":
        text = pathlib.Path(file).read_text(encoding="utf-8")
        return cls.from_text(text)
