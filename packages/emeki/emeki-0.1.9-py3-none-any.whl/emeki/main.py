import argparse
import sys

from emeki.project_setup import setup_project_UI


def emeki_main():
    """The main function.

    It may be called directly from the command line when
    typing `emeki`."""

    print("Hoi! This is my personal python library.")

    # Define argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--init_pro", help="initialize project", action="store_true")

    # Parse arguments
    args = parser.parse_args(sys.argv[1:])

    # Setup base project
    if args.init_pro:
        setup_project_UI()


def execute():
    """Calls `emeki_main` if module is called directly."""
    if __name__ == "__main__":
        sys.exit(emeki_main())


execute()
