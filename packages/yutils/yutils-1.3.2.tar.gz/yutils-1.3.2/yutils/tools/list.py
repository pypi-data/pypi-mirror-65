#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


def make_list(obj):
    if isinstance(obj, list):
        return obj
    return [obj]


def repr_list(iterator):
    """
    Returns an iterator as a string, representing the list.

    :param iterator: the iterator you wish to represent as a list
    :type iterator: iterator
    :return: representation of your iterator as a list
    :rtype: str
    """
    return "'" + "','".join(str(i) for i in iterator) + "'"
