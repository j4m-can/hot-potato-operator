#! /usr/bin/env python3

import os.path
import logging
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.misc import get_methodname, log_enter_exit


logger = logging.getLogger(__name__)


@log_enter_exit(logfn=print)
def a():
    print("a")


@log_enter_exit(logfn=print)
def a_args(x):
    print(f"a_args x ({x})")


@log_enter_exit(logfn=print)
def a_kwargs(y=100):
    print(f"a_kwargs y ({y})")


@log_enter_exit(logfn=print)
def a_args_kwargs(x, y=2):
    print(f"a _args_kwargs x ({x}) y ({y})")


@log_enter_exit(logfn=print)
def b_args(*args):
    print(f"b _args args ({args})")


@log_enter_exit(logfn=print)
def b_args_kwargs(*args, **kwargs):
    print(f"b_args_kwargs args ({args}) kwargs ({kwargs})")


def c_kwargs(y=100):
    print(f"c_kwargs y ({y})")


if 1:

    class A:
        @log_enter_exit(logfn=print)
        def aa(self):
            print(f"--- {dir()}")
            print(f"--- {dir(locals)}")
            print(f"--- {dir(globals)}")
            print(f"{get_methodname(self)}")
            print(f"** {self.__class__.__name__}")
            print("aa")


if __name__ == "__main__":

    A().aa()
    exit

    print()

    print(f"a ({a})")
    a()

    print(f"a_args ({a_args})")
    a_args(1)

    if 1:
        print(f"a_kwargs ({a_kwargs})")
        a_kwargs(y=200)

    print(f"a_args_kwargs ({a_args_kwargs})")
    a_args_kwargs(100, y=200)

    print(f"b_args ({b_args})")
    b_args(1)

    print(f"b_args_kwargs ({b_args_kwargs})")
    b_args_kwargs(11, y=22)

    print(f"c_kwargs ({c_kwargs})")
    c_kwargs(y=89)

    A().aa()
