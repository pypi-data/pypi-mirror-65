#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.exceptions import WrongDatatype, MissingInput, WrongInputDatatype, CodeMistake, YutilsException
from yutils.tools.list import make_list, repr_list


def istype(object_to_check, types_to_validate):
    """
    See yutils.tools.check_object_type docstring for usage.

    :return: If the object is of that type.
    :rtype: bool
    """
    try:
        check_object_type(object_to_check, types_to_validate)
    except (WrongDatatype, WrongInputDatatype, MissingInput):
        return False
    return True


def check_object_type(object_to_check, types_to_validate, input_name=None):
    """
    This checks the types of an object using a certain syntax:
    Lets say we have an object_to_check and the types_to_validate.
    The object_to_check is the object

    :param object_to_check: the object you wish to check its type, and raise an exception should its type not be correct
    :type object_to_check: ....that's what we're here for....
    :param types_to_validate: defines the wanted types for the object to check:
    :type types_to_validate:
                type - checks that object_to_check is of that type
                        Example: float will make sure object_to_check is a float
                list of types - checks that object_to_check is one of the types in the list
                        Example: [int, float] will make sure object_to_check is either an int or a float
                tuple of types - checks hierarchically:
                                    checks that object_to_check is of the type of the first item,
                                    then checks that each item in object_to_check is of the type of the second item,
                                    etc.
                                 Remember, all types in the tuple except the last must support indexing.
                        Example: (list, str) will make sure object_to_check is a list of strings
                                 (tuple, [int, float]) will make sure object_to_check is a tuple of either ints or floats
                dict - checks that object_to_check is an object. It's type is defined by key 'type',
                       with other keys to be checked as the object's attributes.
                        Example: {'type': Person, 'age': int} will make sure object_to_check is a Person object,
                                 with an 'age' attribute that is an int.
                All values can have as many recursive dimensions as wanted.
    :param input_name: Do not use, this is for recursive inner use.

    More examples
    Lets say we create:

    integer = 13
    string = 'foo'
    int_list = list(range(10))
    input_object = MyObject()
    input_object.num = 3
    input_object.lis = [1, 'bar']
    input_object.3dlist = [[(1, 2, 3), (1, 1, 1)], [('a', 'b', 'c'), [7, 8, 9]]]

    We can send:
    check_object_type(integer, int)
    check_object_type(string, str)
    check_object_type(int_list, (list, int))
    check_object_type(input_object, {'type': MyObject,
                                     'num': int,
                                     'lis': (list, [int, str]),
                                     '3dlist': (list, list, [tuple, list], [int, str])
                                     })

    :raises:
             Because of invalid inputs:
                yutils.exceptions.CodeMistake - When no 'type' key is found (for when types_to_validate is a dict)
                yutils.exceptions.WrongDatatype - When no type type is found when isinstance-ing an object's type
             Exceptions raised by check:
                yutils.exceptions.WrongInputDatatype - When the type is not correct during validation
                yutils.exceptions.MissingInput - When an attribute is missing (for when types_to_validate is a dict)
    """
    input_name = object_to_check.__class__.__name__ if input_name is None else input_name

    if isinstance(types_to_validate, dict):
        if 'type' not in types_to_validate.keys():
            raise CodeMistake("Insert a 'type' key in the type dict for instance type check")
        check_object_type(object_to_check, types_to_validate['type'], input_name)
        _check_types_from_dict(object_to_check, types_to_validate, input_name + '->')

    elif isinstance(types_to_validate, tuple):
        check_object_type(object_to_check, types_to_validate[0], input_name)
        _check_types_from_tuple(object_to_check, types_to_validate[1:], input_name, 1)

    elif isinstance(types_to_validate, list):
        _check_types_from_list(object_to_check, types_to_validate, input_name)

    elif isinstance(types_to_validate, type):
        _check_type(object_to_check, types_to_validate, input_name)

    else:
        WrongDatatype(input_name + '->type', type, type(types_to_validate))


def _check_types_from_dict(object_to_check, types_dict, input_name=""):
    """
    Makes sure self has inputs depending on an input dict.

    :raises: yutils.exceptions.MissingInput - When an attribute is missing (for when types_to_validate is a dict)
             For other check_object_type exceptions, see check_object_type docstring.
    """
    for attrib, types in types_dict.items():
        if attrib == 'type':
            continue
        if not hasattr(object_to_check, attrib):
            raise MissingInput(object_to_check, attrib)

        check_object_type(getattr(object_to_check, attrib), types, input_name + attrib)


def _check_types_from_tuple(object_to_check, types_tuple, input_name, level):
    """
    Recursively iterates and makes sure all iterations are of the needed type

    :raises: See check_object_type docstring
    """
    for i in range(len(object_to_check)):
        next_input_name = input_name + '->dimension{}->'.format(level) if isinstance(types_tuple[0], dict) \
            else input_name + '->dimension{}iteration{}'.format(level + 1, i + 1)
        check_object_type(object_to_check[i], types_tuple[0], next_input_name)

        if len(types_tuple) > 1:
            _check_types_from_tuple(object_to_check[i], types_tuple[1:], input_name, level + 1)


def _check_types_from_list(object_to_check, options, input_name=""):
    """
    Checks if object is ONE of a list of expected types, (given different options)
    """
    if not any(istype(object_to_check, option) for option in options):
        raise WrongInputDatatypeFromOptions(input_name,
                                            "\n" + _get_text(options) + "\n")


def _check_type(object_to_check, dtype, input_name=""):
    """
    Checks if object is of expected type
    :type dtype: type

    :raises:
             Exceptions raised by check:
                yutils.exceptions.WrongInputDatatype - When the type is not correct during validation
    """
    if not isinstance(object_to_check, dtype):
        raise WrongInputDatatype(input_name,
                                 dtype.__name__ ,
                                 type(object_to_check))


# ------------------------------------


def _get_text(types):
    if isinstance(types, list):
        text = " OR ".join([_get_text(t) for t in types])
    elif isinstance(types, tuple):
        text = " OF ".join([_get_text(t) for t in types])
    elif isinstance(types, dict):
        checked_attributes = len(list(dict.keys())) - 1
        text = types['type'] + f'Object with {checked_attributes} checked attributes'
    elif isinstance(types, type):
        return types.__name__
    else:
        raise WrongDatatype('types', type(types), _get_text([list, tuple, dict, type]))

    return "(" + text + ")"


class WrongInputDatatypeFromOptions(YutilsException):
    """
    Gets raised when an input argument isn't the right datatype as was expected, out of a set of options
    """
    _STRING = "Error with input '{name}': expected:\n{expectation}"

    def __init__(self, name, expectation):
        """
        :param name: object name
        :type name: str
        :param expectation: expected set of options for datatype
        :type expectation: str
        """
        super().__init__(
            self._STRING.format(
                name=name,
                expectation=expectation
            )
        )
