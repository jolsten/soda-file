import pathlib
import pytest
from sodafile.flf.utils import Section, LabelFile
from .conftest import sample_files, SampleFile


@pytest.mark.parametrize("sample_file", sample_files)
def test_parse_flf(sample_file: SampleFile):
    text = sample_file.flf.read_text(encoding="utf-8")
    flf = LabelFile.from_text(text)
    assert flf.sections
