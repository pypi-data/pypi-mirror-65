#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.exceptions import InputError


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise InputError('Dict does not recognize more than one positional argument.')

        elif len(args) == 1:
            self._update_from_object(args[0])

        self._update_from_object(kwargs)

        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        self._set_attr(key, value)
        super().__setitem__(key, value)

    def _update_from_object(self, obj):
        if hasattr(obj, 'items'):
            for key, value in obj.items():
                self._set_attr(key, value)
        else:
            for key, value in obj:
                self._set_attr(key, value)

    def _set_attr(self, key, value):
        if not isinstance(key, str):
            raise TypeError("AttributeDict keys should be strings, in order for them to be attributes.")
        setattr(self, key, value)

    def update(self, new_dict):
        self._update_from_object(new_dict)
        super().update(new_dict)
