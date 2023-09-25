from collections import UserDict
from dataclasses import dataclass
from textwrap import TextWrapper
from typing import Optional, Dict


def section_to_unwrapped_line(data: Dict[str, str]) -> str:
    return " ".join([f"{key}={val}" for key, val in data.items()])


@dataclass()
class FLFWriter:
    width: int = 79
    indent: Optional[int] = None

    def write(self, flf_dict: dict) -> str:
        if indent is None:
            indent = max([len(x) for x in flf_dict.keys()]) + 1

        lines = []
        wrapper = TextWrapper(
            width=self.width,
            subsequent_indent=" " * self.indent,
            break_on_hyphens=False,
            break_long_words=False,
        )

        for section, data in flf_dict.items():
            wrapper.initial_indent = f"{section: <{self.indent}}"
            line = section_to_unwrapped_line(data)
            lines.extend(wrapper.wrap(line))

        return "\n".join(lines) + "\n"
