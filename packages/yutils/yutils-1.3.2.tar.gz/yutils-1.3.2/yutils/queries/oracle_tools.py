#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import os

ARABIC_NLS_LANG = 'AMERICAN_AMERICA.AL32UTF8'


def match_arabic_nls_lang():
    os.environ['NLS_LANG'] = ARABIC_NLS_LANG


def format_oracle_field_list(field_name, value_list):
    """
    Takes a list that can be more than 999 values long, and wraps them in SQL OR clauses.
    This is useful because Oracle can only accept lists 1000 values long.

    :param field_name: the name of the column you are querying
    :type field_name: str
    :param value_list: list of your values to format into the query
    :type value_list: list of str

    :return: formatted string containing your new WHERE clause
    :rtype: str
    """
    # creates a list of groups of 999 (each group is a list of values)
    divided_value_lists = (value_list[i:i + 999] for i in range(0, len(value_list), 999))

    # each group is now a string with quotes (creates list of quoted strings)
    values_as_strings = ("'" + "','".join((str(i) for i in single_value_list))
                         for single_value_list in divided_value_lists)

    # joins the quoted strings with 'OR field' clause
    return '({} IN ('.format(field_name) + ') OR {} IN ('.format(field_name).join(values_as_strings) + '))'
