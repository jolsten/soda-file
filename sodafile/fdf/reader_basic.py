from dataclasses import dataclass, field
from typing import Literal, Optional, List
import numpy as np


@dataclass
class FDFReader:
    byte: Literal["MSBF", "LSBF"] = "MSBF"
    size: int = 4096
    rbrp: Optional[int] = None
    rbpl: Optional[int] = None
    rrln: int = 70
    dtype: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.byte == "MSBF":
            self.dtype = f">i2"
        elif self.byte == "LSBF":
            self.dtype = f"<i2"
        else:
            raise ValueError

    def read_file(self, path) -> List[List[int]]:
        records = {}
        with open(path, "rb") as file:
            while block := file.read(self.size):
                ptr = self.rbrp

        blocks = np.fromfile(path, dtype="u1")
        num_complete_blocks = blocks.shape[0] // self.size
        blocks = (
            blocks[0 : num_complete_blocks * self.size]
            .reshape(-1, self.size)
            .view(self.dtype)
        )

        records = {}
        for block in blocks:
            block_seqn = block[0]
            rec_start_count = block[1]

            ptr = self.rbpl
            for rec_idx in range(rec_start_count):
                record = block[ptr : ptr + self.rrln]
                selector = int(record[0])

                if selector not in records:
                    records[selector] = []

                records[selector]
                ptr += self.rrln
            print(block[3], block[73], block[143])

            # print(block_seqn, rec_start_count)

        # print(blocks)
        # print(blocks.shape)
