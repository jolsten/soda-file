import pytest
from hypothesis import given, strategies as st
from sodafile.flf.utils import (
    _wrap_sections,
    _unwrap_sections,
    _dict_to_line,
    _line_to_dict,
)
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
