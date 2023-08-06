import functools
import inspect
import pickle
from pathlib import Path
from typing import Callable

from micro_toolkit.os.filesystem import create_dir_if_needed, create_file_dir_if_needed

cache_strategy = [
    "ALWAYS",
    "ONE_TIME",
    "UNTIL_MODIFIED",
    "UNTIL_TIME"
]


def cache_me(strategy="ALWAYS"):
    def wrapper(func: Callable):
        func_name = func.__name__
        source_file = Path(inspect.getsourcefile(func))
        cache_dir = create_dir_if_needed(source_file.parent / ".cache")

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            cache_file = cache_dir / func_name

            print(cache_file)

            if cache_file.exists():
                # read data from file and return
                with cache_file.open("rb") as fd:
                    data = pickle.load(fd)
                    return data
            else:
                data = func(*args, **kwargs)

                # write data to file
                # # create cache dir if not exists yet
                create_file_dir_if_needed(cache_file)

                with cache_file.open('wb') as fd:
                    pickle.dump(data, fd)

                return data

        return decorated

    return wrapper
