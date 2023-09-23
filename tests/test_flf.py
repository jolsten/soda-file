import pytest
from hypothesis import given, strategies as st, given, assume
from sodafile.flf.utils import Section, LabelFile
from sodafile.flf.utils import (
    _wrap_sections,
    _unwrap_sections,
    _dict_to_line,
    _line_to_dict,
    _determine_indent,
)
from .conftest import sample_files, SampleFile
from . import strategies as cst


@given(cst.unwrapped_sections())
def test_wrap_line_length(unwrapped_section):
    text = _wrap_sections([unwrapped_section], indent=cst.INDENT_SIZE)
    for line in text.splitlines(keepends=True):
        assert len(line) == 80


@given(cst.unwrapped_sections())
def test_wrap_unwrap(input):
    input = [input]
    wrapped = _wrap_sections(input, indent=cst.INDENT_SIZE)
    unwrapped = _unwrap_sections(wrapped)
    print("input  =", input)
    print("output =", unwrapped)
    assert input == unwrapped


@given(st.lists(cst.unwrapped_sections(), min_size=3, max_size=8))
def test_wrap_unwrap_many(input):
    wrapped = _wrap_sections(input, indent=cst.INDENT_SIZE)
    unwrapped = _unwrap_sections(wrapped)
    print("input  =", input)
    print("output =", unwrapped)
    assert input == unwrapped


@given(cst.key_val_dict())
def test_dict_to_line(input):
    text = _dict_to_line(input)
    assert len(text.split()) == len(input)


@given(cst.key_val_dict())
def test_dict_to_line_to_dict(input):
    text = _dict_to_line(input)
    output = _line_to_dict(text)
    assert input == output


@given(
    st.integers(min_value=8, max_value=16),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=4, max_size=16),
)
def test_determine_indent(indent, section_name):
    assume(len(section_name) < indent)
    rest = "xxx=xxx " * 4
    line = f"{section_name: <{indent}}{rest}"
    output = _determine_indent(line)
    assert indent == output


@given(cst.unwrapped_sections())
def test_read_write_section(unwrapped):
    sect = Section.from_unwrapped_line(unwrapped)
    output = sect.to_unwrapped_line(cst.INDENT_SIZE)
    assert unwrapped == output


@pytest.mark.parametrize("sample_file", sample_files)
def test_read_flf(sample_file: SampleFile):
    text = sample_file.flf.read_text(encoding="utf-8")
    flf = LabelFile.from_text(text)
    print(flf.sections)
    assert flf.sections


@pytest.mark.parametrize("sample_file", sample_files)
def test_read_write_flf(sample_file: SampleFile):
    text = sample_file.flf.read_text(encoding="utf-8")
    flf = LabelFile.from_text(text)
    output = flf.to_text()

    for a, b in zip(text.splitlines(), output.splitlines()):
        print(f" IN:<{a}>")
        print(f"OUT:<{b}>")
        assert a.strip() == b.strip()
