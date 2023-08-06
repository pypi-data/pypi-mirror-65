import os
from pathlib import Path
from typing import List, Tuple
import datetime

from pkg_resources import resource_filename

from emeki.util import create_dir, zip_dir, unzip_to, str2bool, empty_dir

DATA_DIR = os.path.join(Path(__file__).parent, "template", "project_templates")
ZIP_F_NAME = resource_filename(__name__, f"template/template.zip")

Rule_T = List[Tuple[str, str]]


ALLOWED_EXT = [
    "py",
    "in",
    "txt",
    "rst",
    "md",
    "gitignore",
    "LICENSE",
    "ps1",
]


def repl_in_str(s: str, rep_rules: Rule_T) -> str:
    """Applies a series of replacements to a string."""
    contents = s
    for s1, s2 in rep_rules:
        contents = contents.replace(s1, s2)
    return contents


def repl_in_file(file_path: str, dest_path: str, rep_rules: Rule_T) -> None:
    """Applies a set of replacements to the specified file's content.

    And saves it at `dest_path`."""
    with open(file_path, "r") as f:
        contents = f.read()

    contents = repl_in_str(contents, rep_rules)

    with open(dest_path, "w") as f:
        f.write(contents)


def copy_and_modify_recursive(
    curr_path: str, curr_target_dir: str, rep_rule: Rule_T
) -> None:
    """Copies a folder recursively and applies renaming."""
    if os.path.isdir(curr_path):
        create_dir(curr_target_dir)
        for f in os.listdir(curr_path):
            f_path = os.path.join(curr_path, f)
            f_mod = repl_in_str(f, rep_rule)
            next_target_dir = os.path.join(curr_target_dir, f_mod)
            copy_and_modify_recursive(f_path, next_target_dir, rep_rule)
    else:
        if curr_path.split(".")[-1] in ALLOWED_EXT:
            print(curr_path)
            repl_in_file(curr_path, curr_target_dir, rep_rule)
            # TODO: Include images, but copy only!


def modify_recursively(curr_path: str, rep_rule: Rule_T) -> None:
    """Renames files and folders recursively."""
    if os.path.isdir(curr_path):
        for f in os.listdir(curr_path):
            f_path = os.path.join(curr_path, f)
            f_mod = repl_in_str(f, rep_rule)
            f_path_mod = os.path.join(curr_path, f_mod)
            os.rename(f_path, f_path_mod)
            modify_recursively(f_path_mod, rep_rule)
    else:
        if curr_path.split(".")[-1] in ALLOWED_EXT:
            print(curr_path)
            repl_in_file(curr_path, curr_path, rep_rule)


def create_rules(project_name: str, author: str) -> Rule_T:
    """Creates the replacement rules."""
    project_name_under = project_name.replace("-", "_")
    rep_rules = [
        ("PROJECT_NAME_UNS", project_name_under),
        ("PROJECT_NAME", project_name),
        ("AUTHOR", author),
        ("CURRENT_YEAR", f"{datetime.datetime.now().year}"),
    ]
    return rep_rules


def setup_project(target_dir: str, project_name: str, author: str) -> None:
    """Sets up a sample project."""
    print("This is deprecated!")
    rep_rules = create_rules(project_name, author)
    copy_and_modify_recursive(DATA_DIR, target_dir, rep_rules)


def zip_template() -> None:
    """Zips the template."""
    zip_dir(DATA_DIR, ZIP_F_NAME)


def setup_project_zipped(target_dir: str, project_name: str, author: str) -> None:
    """Sets up a sample project."""
    rep_rules = create_rules(project_name, author)
    unzip_to(ZIP_F_NAME, target_dir)
    modify_recursively(target_dir, rep_rules)


def setup_project_UI() -> bool:
    """Asks the user for info and builds the project."""
    print("Setting up a basic project structure.")
    author = input("Author of the project: ")
    project_name = input("Name of the project: ")
    tar_dir = input("Where to put the files? ")
    if " " in project_name:
        print(f"Project name: '{project_name}' cannot contain whitespaces!")
        return False
    if not os.path.isdir(tar_dir):
        print(f"Invalid directory: '{tar_dir}'")
        return False
    else:
        if len(os.listdir(tar_dir)) != 0:
            print(os.listdir(tar_dir))
            msg = "Specified folder is not empty, want to remove contents? (y/ n)"
            inp = input(msg)
            try:
                remove_contents = str2bool(inp)
                if remove_contents:
                    print("Removing contents of folder.")
                    empty_dir(tar_dir)
                else:
                    print("Aborting")
                    return False
            except ValueError:
                print(f"Answer '{inp}' not understood :(")
                return False
        pass
    setup_project_zipped(tar_dir, project_name, author)
    print("Setup successful :)")
    return True
