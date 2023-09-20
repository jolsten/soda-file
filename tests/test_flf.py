import pathlib
import pytest
from sodafile.flf import _get_indent, _line_to_dict, _text_to_dict
from .conftest import sample_files


@pytest.mark.parametrize(
    "indent, sample",
    [
        (10, "SECTION   KEY=VAL KEY=VAL\n"),
        (8, "SECTION KEY=VAL KEY=VAL\n"),
        (8, "     \nSECTION KEY=VAL KEY=VAL\n"),
    ],
)
def test_get_indent(indent, sample):
    assert indent == _get_indent(sample)


@pytest.mark.parametrize(
    "kvp, results",
    [
        ("KEY1=VAL1 KEY2=VAL2", {"KEY1": "VAL1", "KEY2": "VAL2"}),
        ("KEY1=VAL1 KEY1=VAL2 KEY2=VAL3", {"KEY1": "VAL2", "KEY2": "VAL3"}),
        ("KEY1=", {"KEY1": ""}),
        ("KEY2=VAL2=", {"KEY2": "VAL2="}),
    ],
)
def test_line_to_dict(kvp, results):
    d = _line_to_dict(kvp)
    assert d == results


@pytest.mark.parametrize("kvp", ("KEY3=VAL3 CONTINUED",))
def test_line_to_dict_exc(kvp):
    with pytest.raises(ValueError):
        _line_to_dict(kvp)


@pytest.mark.parametrize("file", sample_files)
def test_text_to_dict(file: str):
    assert _text_to_dict(pathlib.Path(file).read_text(encoding="utf-8"))
