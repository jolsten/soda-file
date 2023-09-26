from hypothesis import given, strategies as st
from sodafile.flf.utils import dict_lower, dict_upper
from .. import strategies as cst


@given(cst.key_val_dict(case="upper"))
def test_dict_lower(data):
    result = dict_lower(data)
    for key, _ in result.items():
        assert key == key.lower()


@given(cst.key_val_dict(case="lower"))
def test_dict_upper(data):
    result = dict_upper(data)
    for key, _ in result.items():
        assert key == key.upper()
