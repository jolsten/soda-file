from typing import TypedDict


class Section(dict):
    pass


class LabelFile(TypedDict):
    volume: Section
    file: Section
    event: Section
    processor: Section
