from dataclasses import dataclass, field
from typing import List, Literal, Optional
import numpy as np


@dataclass
class Record:
    pass


@dataclass
class Block:
    data: np.ndarray
    rbrp: Optional[int] = None
    rbpl: Optional[int] = None
    header_dtype = field(init=False, repr=False)

    def __post_init__(self) -> None:
        header = [
            ("block_sequence_number", "i2"),
            ("record_start_count", "i2"),
        ]
        if self.rbpl is None:
            header.append(("rbpl", "i2"))

        if self.rbrp is None:
            header.append(("rbrp", "i2"))

        self.header_dtype = header
        self.header = self.data[0 : self.rbrp]

    @property
    def block_sequence_number(self) -> int:
        return self.header[0]

    @property
    def record_start_count(self) -> int:
        return self.header[1]


@dataclass
class FDFReader:
    byte: Literal["MSBF", "LSBF"] = "MSBF"
    size: int = 4096
    rbrp: Optional[int] = None
    rbpl: Optional[int] = None
    dtype: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.byte == "MSBF":
            self.dtype = f">i2"
        elif self.byte == "LSBF":
            self.dtype = f"<i2"
        else:
            raise ValueError

    def read_block(self, data: np.ndarray) -> Block:
        return Block(data, rbrp=self.rbrp, rbpl=self.rbpl)

    def read_file(self, path: str) -> List[Block]:
        blocks = np.fromfile(path, dtype="u1").reshape(-1, self.size)
