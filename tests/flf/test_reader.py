import pytest
from sodafile.flf.reader import FLFReader
from ..conftest import sample_files


@pytest.mark.parametrize("sample_file", sample_files)
def test_read_flf(sample_file):
    reader = FLFReader.from_file(sample_file.flf)
    assert reader.data
