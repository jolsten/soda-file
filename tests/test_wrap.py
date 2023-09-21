import pytest
from sodafile.flf.generic import _wrap_sections, _unwrap_sections


@pytest.mark.parametrize(
    "sections",
    [
        [
            "SECTION KEY1=VAL1 KEY2=VALUE2 KEYKEY3=VALUEVALUE3 KEYFOUR=VALUEFOUR KEYFIVEFIVE=VALFIVEFIVE"
        ],
        [
            "NEWSECT KEY1=VAL1 KEY2=VALUE2 KEYKEY3=VALUEVALUE3 KEYFOUR=VALUEFOUR KEYFIVEFIVE=VALFIVEFIVE"
        ],
    ],
)
class TestWrapUnwrapSections:
    def test_wrap_lines(self, sections):
        print("aaa", sections)
        text = _wrap_sections(sections, indent=10)
        for line in text.splitlines(keepends=True):
            assert len(line) == 80
