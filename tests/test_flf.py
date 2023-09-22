import pathlib
import pytest
from sodafile.flf.utils import Section, LabelFile
from .conftest import sample_files, SampleFile
from . import strategies as cst


@given(cst.unwrapped_sections())
def test_read_write_section(sample_files: SampleFile):
    text = sample_files.flf.read_text(encoding="utf-8")
    sect = Section.from_unwrapped_line(text)
    output = sect.to_unwrapped_line()
    assert text == output


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
