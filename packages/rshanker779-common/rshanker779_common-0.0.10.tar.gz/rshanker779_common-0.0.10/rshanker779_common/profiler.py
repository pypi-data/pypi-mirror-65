import cProfile
import datetime
import pathlib
import subprocess
import tempfile
from typing import Callable, Optional
import rshanker779_common as utils

logger = utils.get_logger(__name__)


class Profiler:
    def __init__(
        self, function: Callable, *args, num_iterations: Optional[int] = None, **kwargs
    ):
        """
        :param function: Any function
        :param num_iteration: Number of calls to function
        :param args: Any args for the callable
        :param kwargs: Any kwargs for the callable
        """
        self.raw_function = function
        self.num_iterations = num_iterations
        self.filename = None
        if num_iterations is None:
            _, elapsed = utils.function_timer(self.raw_function, *args, **kwargs)
            estimated_iterations = int(1 / elapsed)
            logger.info(f"Running profile with {estimated_iterations} iterations")
            self.num_iterations = estimated_iterations

        def func():
            for _ in range(self.num_iterations):
                function(*args, **kwargs)

        self._func = func
        self.temporary_directory = tempfile.mkdtemp()

    def profile(self):
        filename = "{}_{}.prof".format(
            self.raw_function.__name__,
            datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S"),
        )
        self.filename = pathlib.Path(self.temporary_directory, filename)

        cProfile.runctx("self._func()", globals(), locals(), self.filename)

    def get_snakeviz_visualisation(self):
        return subprocess.run(["snakeviz", self.filename])  # pragma: no cover
