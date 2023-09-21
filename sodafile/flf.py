import logging
import pathlib
import re
from typing import Dict, List, Optional, Union

_SECTION = re.compile(r"^(?P<section>\S+\s+)(?P<values>.*)$")


def _line_to_dict(value: str) -> dict:
    result = {}
    for kvpair in value.strip().split():
        key, val = kvpair.split("=", maxsplit=1)
        result[key] = val
    return result


def _text_to_dict(text: str) -> dict:
    results: Dict[str, Union[dict, List[dict]]] = {}
    section = None
    for line_no, line in enumerate(text.splitlines()):
        # New SECTION label found
        if m := _SECTION.match(line.strip()):
            section = m.group("section").strip()
            value = m.group("values")

            if section in ("COMMENT", "COMMENTS"):
                results[section] += " " + value.strip()
            # If a SECTION label has not appeared yet, add it as a new dict
            elif section not in results:
                results[section] = _line_to_dict(value)
            # If a SECTION label appears more than once, convert it to a list of dicts instead
            elif not isinstance(results[section], list):
                results[section] = [results[section]]
                results[section].append(_line_to_dict(value))
        # Append to COMMENTS section
        elif section in ("COMMENT", "COMMENTS"):
            results[section] += line.strip()
        # Continuation of previous label section
        elif section:
            if isinstance(results[section], list):
                results[section][-1].update(_line_to_dict(line))
            else:
                results[section].update(_line_to_dict(line))

    return results


def _add_section(section: str, d: dict, indent: int) -> str:
    rest = " ".join([f"{key}={val}" for key, val in d.items()])
    return f"{section: <{indent}}{rest}"


def _assemble_selector_section(meta: dict, selector: int, indent: int) -> List[str]:
    sections = []
    for section, values in meta.items():
        if isinstance(values, list):
            sections.append(_add_section(section, values[selector - 1], indent))
    return sections


def _dict_to_text(meta: dict, indent: Optional[int] = None) -> str:
    if not indent:
        indent = max([len(s) for s in meta.keys()]) + 1
    sections = []
    for section, values in meta.items():
        if isinstance(values, list) and section == "SELECTOR":
            for selector in range(len(values)):
                more = _assemble_selector_section(meta, selector + 1, indent)
                sections.extend(more)
        elif isinstance(values, list):
            pass
        else:
            sections.append(_add_section(section, values, indent))
    return "\n>>>>>".join(sections)


def _get_indent(text: str) -> int:
    line = text.strip().splitlines()[0]
    _, rest = line.split(maxsplit=1)
    return line.find(rest)


class FLF:
    def __init__(
        self, mapping: Optional[Dict[str, Union[dict, List[dict]]]] = None
    ) -> None:
        self._data = mapping
        self._indent: Optional[int] = None
        self._path: Optional[str] = None

    @classmethod
    def from_text(cls, text: str) -> "FLF":
        obj = cls(mapping=_text_to_dict(text))
        obj._indent = _get_indent(text)
        return obj

    @classmethod
    def from_file(cls, file: str) -> "FLF":
        text = pathlib.Path(file).read_text(encoding="utf-8")
        obj = cls.from_text(text)
        obj._path = str(file)
        return obj
