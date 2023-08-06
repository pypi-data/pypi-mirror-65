#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import itertools


def equivilence(iterator, func):
    """
    Divides an iterator to groups, based on the function's result of every item in the iterator.
    Returns dict of lists.

    Example:
        >>> equivilence(range(10), lambda x: x % 3)
        >>>out>>> {0: [0, 3, 6, 9],
        >>>out>>>  1: [1, 4, 7],
        >>>out>>>  2: [2, 5, 8]}

    :param iterator: an iterator you wish to run on and divide into groups
    :type iterator: iterator
    :param func: a function to activate on each iterator item - its result decides the return dict's keys.
    :type func: function

    :rtype: dict of lists (lists are groups of original iterator)
    """
    return_dict = {}
    for item in iterator:
        return_dict.setdefault(func(item), []).append(item)
    return return_dict


def equivilence_itertools(iterator, func):
    """
    Divides an iterator to groups, based on the function's result of every item in the iterator.
    This is now based on itertools.groupby
    Returns dict of lists.

    Example:
        >>> equivilence(range(10), lambda x: x % 3)
        >>>out>>> {0: [0, 3, 6, 9],
        >>>out>>>  1: [1, 4, 7],
        >>>out>>>  2: [2, 5, 8]}

    :param iterator: an iterator you wish to run on and divide into groups
    :type iterator: iterator
    :param func: a function to activate on each iterator item - its result decides the return dict's keys.
    :type func: function

    :rtype: dict of lists (lists are groups of original iterator)
    """
    data = sorted(iterator, key=func)
    return {key: list(group) for key, group in itertools.groupby(data, func)}


def disperse(n, k):
    """
    Disperses a number n between m different groups.
    The sum of all groups must be smaller or equal to n.
    (Yes, the sum can be smaller - that is, a group of zeros is also an answer)

    The answer will have (n + k)! / (n! k!) groups.

    :param n: The number to disperse between groups
    :type n: int
    :param k: The amount of groups to disperse n into
    :type k: int

    :return: All of the options of dispersion - length of (n + k)! / (n! k!)
    :rtype: list of tuples (of ints)
    """
    options = [()]
    for group in range(k):
        new_options = []
        for option in options:
            remainder = n - sum(option)
            for i in range(remainder + 1):
                new_options.append(option + (i,))
        del options
        options = new_options
    return options


def disperse_length(n, k):
    """
    Returns the amount of solutions for the disperse function above.

    From the docstring of the disperse function:
    Disperses a number n between m different groups.
    The sum of all groups must be smaller or equal to n.
    (Yes, the sum can be smaller - that is, a group of zeros is also an answer)

    The answer will have (n + k)! / (n! k!) groups.

    :param n: The number to disperse between groups
    :type n: int
    :param k: The amount of groups to disperse n into
    :type k: int

    :return: The number of solutions of dispersion
    :rtype: int
    """
    return int(factorial(n + k) / (factorial(n) * factorial(k)))


def factorial(n):
    if n < 1:
        raise Exception('Wrong input for factorial:', n)
    if n == 1:
        return 1
    return factorial(n - 1) * n


def dict_of_options_to_subdicts(dict_of_options):
    items = list(dict_of_options.items())
    keys = [key for key, values in items]
    options = [values for key, values in items]

    results = []
    for group in itertools.product(*options):
        results.append(dict(zip(keys, group)))
    return results
