import cProfile
import datetime
import pathlib
import subprocess
import tempfile
from typing import Callable


class Profiler:
    def __init__(self, function: Callable, num_iterations: int = 100, *args, **kwargs):
        """
        :param function: Any function
        :param num_iteration: Number of calls to function
        :param args: Any args for the callable
        :param kwargs: Any kwargs for the callable
        """
        self.raw_function = function
        self.num_iterations = num_iterations
        self.filename = None
        # TODO - measure function once to estimate profiling iterations
        # Output to a temp dir
        # write some more generic decorators
        # TODO this should be able to be used as a decorator
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
