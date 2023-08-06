import os
from typing import Union
from rshanker779_common import get_logger
import inspect
import pathlib

logger = get_logger(__name__)


def make_dirs(directory: Union[str, bytes]) -> pathlib.Path:
    directory = pathlib.Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def add_init_files(filepath: Union[str, bytes, pathlib.Path]):
    for root, _, files in os.walk(pathlib.Path(filepath)):
        needs_init_file = any(i for i in files if i.endswith(".py") and i != "setup.py")
        has_init_file = any(i for i in files if i == "__init__.py")
        if needs_init_file and not has_init_file:
            logger.info("Adding init file to directory %s", root)
            pathlib.Path(root, "__init__.py").write_text("")


def relative_path(*args: str) -> pathlib.Path:
    frame = inspect.stack()[1]
    file_path = pathlib.Path(frame.filename)
    return pathlib.Path(file_path.parent, *args)
