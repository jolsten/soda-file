import pytest

from sodafile.flf.reader_old import FLFReader

from ..conftest import sample_files


@pytest.mark.parametrize("sample_file", sample_files)
def test_read_flf_from_file(sample_file):
    data = FLFReader.from_file(sample_file.flf)
    assert data


@pytest.mark.parametrize("sample_file", sample_files)
def test_read_flf_from_text(sample_file):
    with open(sample_file.flf, "r") as file:
        text = file.read()
        data = FLFReader.from_text(text)
        assert data
