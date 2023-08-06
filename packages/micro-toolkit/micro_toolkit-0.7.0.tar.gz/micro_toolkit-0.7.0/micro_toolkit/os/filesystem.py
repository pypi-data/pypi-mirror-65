import os
from pathlib import Path
import shutil
from typing import Union


def remove_files_in_dir(data_dir):
    input_file_list = [
        i.absolute() for i in Path(data_dir).iterdir() if i.is_file()
    ]
    for i in input_file_list:
        i.unlink()


def remove_content_in_dir(data_dir):
    input_file_list = Path(data_dir).iterdir()
    for i in input_file_list:
        file_path = str(i.absolute())
        if i.is_dir():
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)


def create_dir_if_needed(directory: Union[str, Path]):
    if isinstance(directory, Path):
        return _create_dir_if_needed_from_path(directory)
    else:
        return _create_dir_if_needed_from_str(directory)


def _create_dir_if_needed_from_str(directory):
    # copied from https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def _create_dir_if_needed_from_path(directory: Path):
    directory.mkdir(mode=0o777, parents=True, exist_ok=True)

    return directory


def create_file_dir_if_needed(file):
    directory = os.path.dirname(file)

    create_dir_if_needed(directory)

    return file
