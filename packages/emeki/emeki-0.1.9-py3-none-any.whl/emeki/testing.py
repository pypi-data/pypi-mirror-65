"""This module provides some additional testing functionality.

"""
import builtins
from typing import List, Union, Callable


class AssertPrints:
    """Checks if `print` is called with the specified arguments.

    Does not capture general stdout output."""

    print_list: List[str] = []
    exp_print: List[str]
    old_print = None
    no_output: bool

    def __init__(self, s: Union[str, List[str]], no_output: bool = False):
        self.exp_print = s if isinstance(s, list) else [s]
        self.no_output = no_output

    def new_print(self, *args):
        self.print_list += [args[0] if len(args) == 1 else args]
        if not self.no_output:
            self.old_print(*args)

    def __enter__(self):
        self.old_print = builtins.print
        builtins.print = self.new_print

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            assert len(self.exp_print) == len(self.print_list)
            for e, p in zip(self.exp_print, self.print_list):
                assert e == p, f"{e} != {p}"
        finally:
            builtins.print = self.old_print

    pass


class InputMock:
    """Mocks the `input()` function.

    The return values for consecutive calls are
    specified in `input_list`.
    """

    count: int = 0
    orig_inp: Callable = None
    input_list: List

    def __init__(self, input_list):
        self.input_list = input_list

    def __enter__(self):
        self.orig_inp = builtins.input
        builtins.input = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.input = self.orig_inp

    def __call__(self, *args, **kwargs):
        ret_val = self.input_list[self.count]
        self.count += 1
        return ret_val
