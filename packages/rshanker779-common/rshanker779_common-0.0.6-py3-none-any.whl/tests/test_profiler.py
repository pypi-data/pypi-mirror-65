import pathlib

import pytest

import rshanker779_common as utils


@pytest.fixture
def example_function():
    def example_string_function(x, y):
        return str(reversed(x)) + y

    return example_string_function


@pytest.fixture
def profiler(example_function):
    return utils.Profiler(example_function, 100, "xfsjkfljkslf", "fkdskfl")


def test_profiler(profiler):
    profiler.profile()
    assert pathlib.Path(profiler.filename).is_file()
