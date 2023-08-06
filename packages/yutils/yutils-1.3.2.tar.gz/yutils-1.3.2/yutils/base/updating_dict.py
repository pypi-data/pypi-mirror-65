#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38


class DictValueList(list):
    pass


class UpdatingDict(dict):
    def __setitem__(self, key, value):
        if key in self.keys():
            old_value = self[key]
            if isinstance(old_value, DictValueList):
                if value in old_value:
                    return
                new_value = DictValueList(old_value + [value])
            else:
                if value == old_value:
                    return
                new_value = DictValueList([old_value, value])
        else:
            new_value = value
        super().__setitem__(key, new_value)

    def update(self, new_dict):
        for key, value in new_dict.items():
            self[key] = value
