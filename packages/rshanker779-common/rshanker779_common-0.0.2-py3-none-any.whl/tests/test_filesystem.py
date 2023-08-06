import rshanker779_common as utils
import pathlib
import tempfile
import os
import pytest


@pytest.fixture
def build_init_directories(tmp_path):
    (tmp_path / "setup.py").write_text("import setuptools")
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "test.py").write_text("")
    (tmp_path / "a" / "b").mkdir()
    (tmp_path / "a" / "b" / "c").mkdir()
    (tmp_path / "a" / "b" / "c" / "nested.py").write_text("")
    yield


def test_init_directories(tmp_path, build_init_directories):
    utils.add_init_files(tmp_path)
    assert not (tmp_path / "__init__.py").is_file()
    assert (tmp_path / "a" / "__init__.py").is_file()
    assert not (tmp_path / "a" / "b" / "__init__.py").is_file()
    assert (tmp_path / "a" / "b" / "c" / "__init__.py").is_file()


def test_relative_path():
    assert utils.relative_path() == pathlib.Path(__file__).parent
    assert utils.relative_path("a", "b") == pathlib.Path(__file__).parent / "a" / "b"


def test_make_dirs(tmp_path):
    res = utils.make_dirs(tmp_path / "example")
    assert (tmp_path / "example").is_dir()
    assert res == (tmp_path / "example")
