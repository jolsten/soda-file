from collections import UserDict
from dataclasses import dataclass
import pathlib
from typing import Union, List, Tuple, Optional


class SectionDict(UserDict):
    def __setitem__(self, key: str, val: dict) -> None:
        if key in self:
            if isinstance(self[key], dict):
                self.data[key] = [self.data[key]]
            self.data[key].append(val)
        else:
            self.data[key] = val

    def __getitem__(self, key: str) -> str:
        if isinstance(key, tuple):
            key, selector = key
            return self.data[key.upper()][selector - 1]
        return self.data[key.upper()]

    def update(self, section: str, data: Union[dict, str]):
        if isinstance(data, dict):
            if isinstance(self.data[section], list):
                self.data[section][-1].update(data)
            else:
                self.data[section].update(data)
        elif isinstance(data, str):
            self.data[section] += " " + data
        else:
            raise TypeError

    def add(self, section: str, data: Union[dict, str]) -> None:
        # If it's a comment, append it to the comments string
        if section in ("COMMENT", "COMMENTS"):
            if section not in self.data:
                self.data[section] = ""
            self.data[section] += " " + data.strip()
        elif section not in self.data:
            self.data[section] = data
        elif isinstance(self.data[section], dict):
            self.data[section] = [self.data[section]]
            self.data[section].append(data)


def parse_line(line: str) -> Tuple[str, dict]:
    section, rest = line.split(" ", maxsplit=1)
    if section in ("COMMENT", "COMMENTS"):
        return section, rest.strip()
    meta = {}
    for kvp in rest.split():
        try:
            key, val = kvp.split("=", maxsplit=1)
            meta[key] = val
        except ValueError:
            pass
    return section, meta


@dataclass
class FLFReader:
    data: SectionDict

    def get_section(self, name: str) -> Union[dict, List[dict], str]:
        name = name.upper()
        return self.data[name] if name in self.data else {}

    def get_value(self, section: str, key: str, selector: Optional[int] = None) -> str:
        sect = self.get_section(section.upper())
        if selector:
            sect = sect[selector - 1]
        return sect.get(key.upper(), None)

    def to_dict(self) -> dict:
        return dict(self.data)

    @classmethod
    def from_text(cls, text: str) -> "FLFReader":
        sect = SectionDict()
        current_section = None
        for line_no, line in enumerate(text.splitlines()):
            if line.strip() == "":  # Skip empty lines
                continue

            section, data = parse_line(line)

            # If section is truthy, it is not empty string ""
            # so add it as a new section
            if section:
                sect.add(section, data)
                current_section = section
            # If section is falsey, it is empty string ""
            # so add key-val-pairs to current section
            else:
                sect.update(current_section, data)
        return cls(sect)

    @classmethod
    def from_file(cls, path) -> "FLFReader":
        text = pathlib.Path(path).read_text(encoding="utf-8")
        return cls.from_text(text)

    @property
    def selectors(self) -> Tuple[int]:
        if isinstance(self.data["SELECTOR"], list):
            return tuple([int(data["NUMBER"]) for data in self.data["SELECTOR"]])
        return (1,)

    def selector(self, number: int) -> "FLFReader":
        if number not in self.selectors:
            raise ValueError(f"Invalid selector number: {number}")

        new_data = SectionDict()
        for section, data in self.data.items():
            if isinstance(data, list):
                new_data[section] = data[number - 1]
            else:
                new_data[section] = data
        return new_data
