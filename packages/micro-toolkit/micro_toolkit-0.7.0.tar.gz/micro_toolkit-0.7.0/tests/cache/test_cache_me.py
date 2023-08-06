import os
import shutil
from pathlib import Path

from micro_toolkit.cache.cache_me import cache_me


def test_cache_me():
    func_run_flag = False

    @cache_me()
    def func():
        nonlocal func_run_flag
        func_run_flag = True

        return "hello, world"

    # run first time
    # # remove cache file in case of multi running with crash
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    cache_path = current_path / ".cache"
    shutil.rmtree(cache_path)

    result = func()

    assert func_run_flag
    assert result == "hello, world"

    # run second time
    # # reset flag
    func_run_flag = False

    result = func()
    assert not func_run_flag
    assert result == "hello, world"

    # clean up
    shutil.rmtree(cache_path)
