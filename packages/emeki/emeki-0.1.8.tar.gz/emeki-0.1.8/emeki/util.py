"""The util module.

This module provides some utility functionality.
"""
import os
import shutil
import zipfile


def str2bool(v) -> bool:
    """Converts a string to a boolean.

    Raises:
        ValueError: If it cannot be converted.
    """
    if isinstance(v, bool):
        return v
    elif isinstance(v, str):
        v_low = v.lower()
        if v_low in ("yes", "true", "t", "y", "1", "1.0"):
            return True
        elif v_low in ("no", "false", "f", "n", "0", "0.0"):
            return False
    raise ValueError(f"{v} is not convertible to boolean!")


def create_dir(dir_name: str) -> None:
    """Creates the given directory recursively.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return


def empty_dir(dir_name: str) -> None:
    """Removes the content of the specified directory."""
    for f in os.listdir(dir_name):
        f_path = os.path.join(dir_name, f)
        if os.path.isdir(f_path):
            shutil.rmtree(f_path)
        else:
            os.remove(f_path)


def zip_dir(dir_path: str, save_path: str):
    """Zips and saves a directory."""
    assert save_path[-4:] == ".zip"
    path_no_zip = save_path[:-4]
    shutil.make_archive(path_no_zip, "zip", dir_path)


def unzip_to(file_to_unzip: str, dest_dir: str):
    """Extract all the contents of zip file in `dest_dir`."""
    with zipfile.ZipFile(file_to_unzip, "r") as zipObj:
        zipObj.extractall(dest_dir)
