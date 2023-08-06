import time
import datetime
from typing import Callable, Optional, Tuple, Any
from functools import wraps, partial

from rshanker779_common import get_logger

logger = get_logger(__name__)


def function_timer(f: Callable, *args, **kwargs) -> Tuple[Any, float]:
    s = time.perf_counter()
    res = f(*args, **kwargs)
    elapsed = time.perf_counter() - s
    return res, elapsed


def time_it(f: Callable):
    @wraps(f)
    def wrapper_func(*args, **kwargs):
        function_return, elapsed = function_timer(f, *args, **kwargs)
        logger.info(f"{f.__name__} executed in {elapsed:2f} seconds")
        return function_return

    return wrapper_func


class ErrorCatchDecorator:
    def __init__(
        self, number_retries: Optional[int], time_retry: Optional[datetime.timedelta]
    ):
        self.number_retries = number_retries
        self.time_retry = time_retry
        if self.number_retries is None and self.time_retry is None:
            self.number_retries = 3

    def __call__(self, f):
        @wraps(f)
        def wrapped_func(*args, **kwargs):
            for _ in range(self.number_retries):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    logger.exception(
                        f"Error calling {f.__name__} with arguments {args}, {kwargs}"
                    )
                    if self.time_retry is not None:
                        time.sleep(self.time_retry.total_seconds())

        return wrapped_func


def catch_errors(f):
    return ErrorCatchDecorator(1, None)(f)


def retry(f=None, *, number_retries=None, time_retry=None):
    error_decorator = ErrorCatchDecorator(number_retries, time_retry)
    if f is None:
        return error_decorator
    return error_decorator(f)
