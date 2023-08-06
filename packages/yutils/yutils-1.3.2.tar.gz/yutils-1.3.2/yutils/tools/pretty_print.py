#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools.list import repr_list

LONG_VALUE_LIMIT = 120
LONG_VALUE_FILLER = '<Long {type} object with repr length {length}>'


def pprint_dict(dictionary, long_value_limit=LONG_VALUE_LIMIT, long_value_filler=LONG_VALUE_FILLER):
    """
    Prints a dict in a very pretty way!

    :param dictionary: your dict to print
    :type dictionary: dict
    :param long_value_limit: when a dict value exceeds this limit, it won't be printed
                             Default: 120
    :type long_value_limit: int
    :param long_value_filler: A filler to print instead of a long value, must have {type} and {length} fields!
                              Default: '<Long {type} object with repr length {length}>'
    :type long_value_filler: str
    :return: None
    """
    indent_len = max([len(str(key)) for key in dictionary.keys()]) + 2
    for key, value in dictionary.items():
        repr_value = repr(value)
        if len(repr_value) > long_value_limit:
            repr_value = long_value_filler.format(type=type(value).__name__,
                                                  length=len(repr_value))
        print('{key}:{spaces}{value}'.format(
            key=key,
            spaces=' '*(indent_len - len(str(key))),
            value=repr_value
        ))


def pprint_list(list_to_print):
    """
    Prints a list in an easy, short way.

    :param list_to_print: the list you wish to print
    :type list_to_print: list
    :return: None
    """
    print(repr_list(list_to_print))
