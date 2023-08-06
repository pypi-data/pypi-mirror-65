#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


class ColorsConsts:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


COLOR_TRANSLATION = {'pink': ColorsConsts.PINK,
                     'p': ColorsConsts.PINK,
                     'blue': ColorsConsts.BLUE,
                     'b': ColorsConsts.BLUE,
                     'green': ColorsConsts.GREEN,
                     'g': ColorsConsts.GREEN,
                     'yellow': ColorsConsts.YELLOW,
                     'y': ColorsConsts.YELLOW,
                     'red': ColorsConsts.RED,
                     'r': ColorsConsts.RED}


def print_color(text, color):
    color_str = COLOR_TRANSLATION[color.lower()]
    print(color_str + text + ColorsConsts.END)
