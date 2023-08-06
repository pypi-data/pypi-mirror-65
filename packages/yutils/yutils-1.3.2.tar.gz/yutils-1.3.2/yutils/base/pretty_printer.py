#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from collections import OrderedDict

from yutils.tools import pprint_dict


class PrintableObject(object):
    """
    An object you can derive from, that has a pprint method - printing all set attributes
    """
    def __init__(self):
        self._fields = []

    def __setattr__(self, key, value):
        if hasattr(self, '_fields') \
                and key \
                and key not in self._fields \
                and key[0] != '_':
            self._fields.append(key)

        super().__setattr__(key, value)

    def _create_ordered_dict(self):
        o_dict = OrderedDict()
        for field in self._fields:
            o_dict[field] = getattr(self, field)
        return o_dict

    def pprint(self):
        print(str(self))

        all_fields = self._create_ordered_dict()
        pprint_dict(all_fields)
        del all_fields
