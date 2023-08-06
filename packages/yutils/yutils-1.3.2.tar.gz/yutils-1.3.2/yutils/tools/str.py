#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

TYPES_TO_ASSESS = [int, float]


def turn_numeric(string):
    """
    Turns a string into either an int or a float

    :param string: a string to assess
    :type string: str

    :rtype: str or float

    :raises: TypeError if no type was found
    """
    for conversion_type in TYPES_TO_ASSESS:
        try:
            return conversion_type(string)
        except ValueError:
            pass

    raise TypeError(f"String: '{string}' is not one of these types: '{TYPES_TO_ASSESS!r}'")
