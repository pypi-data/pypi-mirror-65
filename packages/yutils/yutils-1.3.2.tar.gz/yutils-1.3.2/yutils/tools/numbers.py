#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import math


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    ans = math.floor(n * multiplier + 0.5) / multiplier
    if decimals <= 0:
        ans = int(ans)
    return ans
