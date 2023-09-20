import pytest
import pathlib


def find_sample_files():
    return list(pathlib.Path("data/").glob("**/*.flf"))


sample_files = find_sample_files()
