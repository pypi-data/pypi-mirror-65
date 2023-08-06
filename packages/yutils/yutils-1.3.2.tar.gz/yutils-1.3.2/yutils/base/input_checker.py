#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools import check_object_type, prioritize_dicts
from yutils.exceptions import InputError, WrongDatatype, CodeMistake
from yutils.base.attribute_dict import AttributeDict


class InputChecker(object):
    _INPUT_TYPES = {}
    _INPUT_OPTIONS = {}
    _INPUT_DEFAULTS = {}
    _INPUT_ALTERNATIVES = []

    _INVALID_INPUT_OPTION_EXCEPTION_STR = 'Input {input} was {reality} but should be one of these options:\n{options}'

    def __init__(self, **inputs):
        """
        Base object for making a Python object more static-typed.
        It is useful for checking __init__ argument inputs (type and content).

        Type check is defined by _INPUT_TYPES class constant. (see yutils.tools.check_object_type for usage)
        Option check is defined by _INPUT_OPTIONS class constant.
        Default input options are defined by _INPUT_DEFAULTS class constant.
        Input alternatives are defined by _INPUT_ALTERNATIVES class constant.

        This also:
            - creates self._inputs as the inputs dict given, with defaults, as an AttributeDict.
            - creates self._inputs_without_defaults as only the inputs dict given, without defaults, as an AttributeDict.
            - adds each input in inputs as an attribute to your object.
                (Including values of _INPUT_DEFAULTS if inputs aren't otherwise present)

        :param inputs: your __init__ inputs, can be anything you wish to check

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        """
        self._create_input_checker_attributes(inputs)
        self._check_input_checker_inputs()

    def _create_input_checker_attributes(self, inputs):
        """
        1. Creates self._inputs as the inputs dict given, as an AttributeDict.
        2. Adds each input in inputs as an attribute to your object.

        :param inputs: the inputs given as Keyword Arguments to __init__
        :type inputs: dict
        """
        self._inputs_without_defaults = AttributeDict(inputs)

        all_inputs = prioritize_dicts(inputs, self._INPUT_DEFAULTS)
        self._inputs = AttributeDict(all_inputs)

        for key, value in all_inputs.items():
            setattr(self, key, value)

    def _check_input_checker_inputs(self):
        """
        Checks all inputs (types and contents).
        This also makes sure self._INPUT_TYPES and self._INPUT_OPTIONS are dicts, as expected.

        See yutils.tools.check_object_type for documentation on _INPUT_TYPES format and usage.

        :raises: yutils.exceptions.WrongDatatype if any input is not of the specified type, defined by _INPUT_TYPES
                 yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS

        """
        if not isinstance(self._INPUT_TYPES, dict):
            raise WrongDatatype('_INPUT_TYPES', dict, type(self._INPUT_TYPES))
        if not isinstance(self._INPUT_OPTIONS, dict):
            raise WrongDatatype('_INPUT_OPTIONS', dict, type(self._INPUT_OPTIONS))
        check_object_type(self._INPUT_ALTERNATIVES, (list, list, [str, (tuple, str)]))

        self._check_input_checker_input_types()
        self._check_input_checker_input_options()
        self._check_input_checker_input_alternatives()

    def _check_input_checker_input_types(self):
        types_dict = {'type': InputChecker}
        types_dict.update(self._INPUT_TYPES)
        check_object_type(self, types_dict)

    def _check_input_checker_input_options(self):
        """
        Uses self._INPUT_OPTIONS to make sure given inputs are in wanted options defined.

        :raises: yutils.exceptions.InputError if any input is not one of the options, defined by _INPUT_OPTIONS
        """
        for input_str, options in self._INPUT_OPTIONS.items():
            input_val = getattr(self, input_str)
            if input_val not in options:
                raise InputError(self._INVALID_INPUT_OPTION_EXCEPTION_STR.format(input=input_str,
                                                                                 reality=input_val,
                                                                                 options=repr(options)))

    def _check_input_checker_input_alternatives(self):
        """
        Uses self._INPUT_ALTERNATIVES to check if the user gave one (and only one) of the alternatives for inputs.

        Each item in the list self._INPUT_ALTERNATIVES is a different combination to check, and should be a list.
            Each item in the combination list should be an alternative input option.
                This option can be either a string (a single input name) or a tuple of strings (a combination of a few inputs).

        For example:
            self._INPUT_ALTERNATIVES = [
                                        ['foo', 'bar'],
                                        [('a', 'b'), ('x', 'y', 'z')]
                                       ]
            Will make sure that:
                    * foo is None and bar is not None (or vice versa)
                    * a and b are None, and x, y, and z are not None (or vice versa)

        :raises: yutils.exceptions.InputError if any alternative is not met
        """
        for combination in self._INPUT_ALTERNATIVES:
            alternative_met = False
            for alternative in combination:
                alternative_given = self._check_input_checker_alternative_given(alternative)

                if alternative_given and not alternative_met:
                    alternative_met = True
                elif alternative_given:
                    raise InputAlternativesError(combination, 1)
            if not alternative_met:
                raise InputAlternativesError(combination, 0)

    def _check_input_checker_alternative_given(self, alternative):
        if isinstance(alternative, tuple):
            return all(self._check_input_checker_alternative_given(item) for item in alternative)

        try:
            return getattr(self, alternative) is not None
        except AttributeError:
            raise CodeMistake(f"Alternative '{alternative}' attribute doesn't exist.")


class InputAlternativesError(InputError):
    """
    Gets raised when the input wasn't as expected (e.g. isn't a valid option),
        because either none or more than one input alternatives were met.
    """

    _ERROR_STR = 'You must give as inputs either:\n'
    _MULTIPLE_SUFFIX = '\n(But not more than one of them)'

    def __init__(self, combination, flag):
        """
        :param combination: set of alternatives to print
        :type combination: list, of: strings or tuples of strings

        :param flag: 0 if no alternative was met
                     1 if more than one alternative was met
        :type flag: int
        """
        error_msg = self._ERROR_STR
        error_msg += self.create_alternatives_string(combination)
        if flag:
            error_msg += self._MULTIPLE_SUFFIX
        super().__init__(error_msg)

    @staticmethod
    def create_alternatives_string(combination):
        lines = []
        for alternative in combination:
            if isinstance(alternative, tuple):
                alternative = " AND ".join(alternative)
            lines.append(alternative)
        return "\n    OR\n".join(lines)
