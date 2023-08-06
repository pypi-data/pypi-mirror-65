#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


def prioritize_dicts(*dicts):
    """
    Creates a new dict, prioritizing a more previous dict's keys/values from a later dict's keys/values.
    All of the first dict's keys/values will be present in the return dict.
    The other dicts' keys/values will be present only if no previous dictionaries had the same key.

    :param dicts: any number of dictionaries to prioritize between.
    :type dicts: dicts

    :return: A final dict
    :rtype: dict
    """
    final_dict = {}
    for dct in dicts:
        for key, value in dct.items():
            if key not in final_dict:
                final_dict[key] = value
    return final_dict
