import pathlib

import pytest

import rshanker779_common as utils


@pytest.fixture
def example_function():
    def example_string_function(x, y):
        return str(reversed(x)) + y

    return example_string_function


def test_profiler(example_function):
    profiler = utils.Profiler(
        example_function, num_iterations=100, x="xfsjkfljkslf", y="fkdskfl"
    )
    profiler.profile()
    assert pathlib.Path(profiler.filename).is_file()


def test_profiler_estimation(example_function):
    profiler = utils.Profiler(example_function, "afdjkla", "dsajdknsa")
    profiler.profile()
    assert profiler.num_iterations > 100_000
    assert profiler.num_iterations < 300_000
