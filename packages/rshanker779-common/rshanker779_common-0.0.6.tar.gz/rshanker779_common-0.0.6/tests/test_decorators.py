import logging

import rshanker779_common as utils


@utils.time_it
def example_function():
    return 1


@utils.catch_errors
def error_function():
    raise ValueError


def test_time_it(caplog):
    with caplog.at_level(logging.INFO):
        res = example_function()
    assert res == 1
    assert len(caplog.messages) == 1
    assert "example_function executed in" in caplog.messages[0]


def test_catch_errors(caplog):
    with caplog.at_level(logging.ERROR):
        res = error_function()
    assert res is None
    assert len(caplog.messages) == 1
    assert "Error calling error_function" in caplog.messages[0]
