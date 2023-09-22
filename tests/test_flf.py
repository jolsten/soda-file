import pathlib
import pytest
from sodafile.flf.utils import Section, LabelFile
from .conftest import sample_files, SampleFile


@pytest.mark.parametrize("sample_file", sample_files)
def test_parse_flf(sample_file: SampleFile):
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
