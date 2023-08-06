#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools.colors import print_color


def verbose_print(verbose, *args, color=None):
    if verbose:
        printer(*args, color=color)


def printer(*args, color=None):
    if color is None:
        print(*args)
    else:
        text = ' '.join('{}'.format(arg) for arg in args)
        print_color(text, color=color)


def ignore(*args, color=None):
    pass


def get_verbose_printer(verbose):
    func = printer if verbose else ignore
    return func
