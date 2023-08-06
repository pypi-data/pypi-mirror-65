import datetime
import logging
import time

import rshanker779_common as utils


@utils.time_it
def example_function():
    return 1


@utils.catch_errors
def error_function():
    raise ValueError


@utils.retry(number_retries=2, time_retry=datetime.timedelta(milliseconds=10))
def error_function_2():
    print(1)
    raise ValueError


@utils.retry
def error_function_3():
    print(1)
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


def test_retry(capsys, caplog):
    start = time.time()
    with caplog.at_level(logging.ERROR):
        res = error_function_2()
    assert res is None
    time_taken = time.time() - start
    out, err = capsys.readouterr()
    assert_retry_logic(caplog, out, time_taken, 2, 0.002, "error_function_2")


def test_default_retry(capsys, caplog):
    start = time.time()
    with caplog.at_level(logging.ERROR):
        res = error_function_3()
    assert res is None
    time_taken = time.time() - start
    out, err = capsys.readouterr()
    assert_retry_logic(caplog, out, time_taken, 3, 0, "error_function_3")


def assert_retry_logic(
    caplog, out, time_taken, expected_count, minimum_time, function_name
):
    assert out.count("1") == expected_count
    assert time_taken > minimum_time
    assert len(caplog.messages) == expected_count
    assert caplog.messages[0] == caplog.messages[1]
    assert f"Error calling {function_name}" in caplog.messages[0]
