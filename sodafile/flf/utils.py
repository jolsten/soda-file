from dataclasses import dataclass, field
import re
from textwrap import TextWrapper
from typing import Dict, List, Optional

NEW_SECTION = re.compile(r"^(?P<section>\S+\s+)(?P<rest>.*)$")
LINE_SIZE = 79


def _determine_indent(text: str) -> int:
    _, rest = text.split(maxsplit=1)
    return text.find(rest)


def _line_to_dict(text: str) -> Dict[str, str]:
    kvpairs = text.strip().split()
    results = {}
    for kvp in kvpairs:
        try:
            key, val = kvp.split("=")
        except ValueError:
            pass
        results[key] = val
    return results


def _dict_to_line(data: Dict[str, str]) -> str:
    return " ".join([f"{key}={val}" for key, val in data.items()])


def _unwrap_sections(text: str) -> List[str]:
    out = ""
    for line in text.splitlines():
        if match := NEW_SECTION.match(line):
            sect = match.group("section")
            rest = match.group("rest").strip()
            out += f"\n{sect}{rest}"
        else:
            out += " " + line.strip()
    return out.lstrip().splitlines()


def _wrap_sections(sections: List[str], indent: int) -> str:
    wrapper = TextWrapper(
        width=LINE_SIZE,
        subsequent_indent=" " * indent,
        break_on_hyphens=False,
        break_long_words=False,
    )

    out = []
    for text in sections:
        # print("section", text)
        section, rest = text.split(maxsplit=1)
        wrapper.initial_indent = f"{section: <{indent}}"
        wrapped = wrapper.wrap(rest)
        out.extend(wrapped)

    out = [f"{line:<{LINE_SIZE}}" for line in out]
    return "\n".join(out) + "\n"


@dataclass
class Section:
    name: str
    values: Dict[str, str]

    @classmethod
    def from_unwrapped_line(cls, text: str) -> "Section":
        name, rest = text.split(maxsplit=1)
        values = _line_to_dict(rest)
        return cls(name=name, values=values)

    def to_unwrapped_line(self, indent: int) -> str:
        return f"{self.name: <{indent}}{_dict_to_line(self.values)}"


@dataclass
class LabelFile:
    sections: List[Section] = field()
    indent: Optional[int] = None

    @classmethod
    def from_text(cls, text: str) -> "LabelFile":
        indent = _determine_indent(text)
        unwrapped = _unwrap_sections(text)
        sections = [Section.from_unwrapped_line(line) for line in unwrapped]
        return cls(sections=sections, indent=indent)

    def to_text(self) -> str:
        indent = self.indent
        if indent is None:
            indent = max([len(sect.name) for sect in self.sections]) + 1
        sections = [sect.to_unwrapped_line(indent) for sect in self.sections]
        text = _wrap_sections(sections, indent)
        return text
