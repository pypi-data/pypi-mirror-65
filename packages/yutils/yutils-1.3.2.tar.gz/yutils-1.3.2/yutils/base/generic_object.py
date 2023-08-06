#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.base.pretty_printer import PrintableObject
from yutils.exceptions import WrongInputDatatype


class GenericObject(PrintableObject):
    """
    A generic object you can easily use for your scripts, with a pprint and a str/repr for easy printing
    """
    def __init__(self, object_name):
        """
        :param object_name: The name for your object!
        :type object_name: str
        """
        if not isinstance(object_name, str):
            raise WrongInputDatatype('object_name', str, type(object_name))

        self._object_name = object_name

        super().__init__()

    def __str__(self):
        return "<{object_name} Object with {num_fields} attrs>".format(
            object_name=self._object_name.capitalize(),
            num_fields=len(self._fields)
        )

    def __repr__(self):
        return str(self)


def dict_to_generic_object(dictionary, object_name):
    """
    Converts a dictionary (recursively) to a GenericObject, with keys as attributes.

    :param dictionary: dictionary to convert (key-values will be converted to attribute-values)
    :type dictionary: dict
    :param object_name: a name for your new object's type
    :type object_name: str
    :return: GenericObject object
    """
    obj = GenericObject(object_name)

    for key, value in dictionary.items():
        key = key if isinstance(key, str) else repr(key)

        if isinstance(value, dict):
            setattr(obj, key, dict_to_generic_object(value, key))
        else:
            setattr(obj, key, value)

    return obj
