from dataclasses import dataclass
import pytest
import pathlib


@dataclass
class SampleFile:
    path: pathlib.Path

    @property
    def flf(self) -> pathlib.Path:
        return self.path.with_suffix(".flf")

    @property
    def fdf(self) -> pathlib.Path:
        return self.path.with_suffix(".fdf")

    @property
    def txt(self) -> pathlib.Path:
        return self.path.with_suffix(".txt")


def find_sample_files():
    return [SampleFile(path) for path in pathlib.Path("data/").glob("**/*.flf")]


sample_files = find_sample_files()
