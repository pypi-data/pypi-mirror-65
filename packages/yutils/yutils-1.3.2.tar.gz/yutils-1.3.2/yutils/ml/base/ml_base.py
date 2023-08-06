#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import re
import numpy as np

from yutils.base import InputChecker
from yutils.exceptions import YutilsException, InputError
from yutils.tools.numpy_tools import to_array, is_matrix, isnt_column_array
from yutils.tools import verbose_print


class MLObject(InputChecker):
    def _verbose_print(self, *args, color=None):
        verbose_print(self.verbose, *args, color=color)

    @staticmethod
    def _add_ones(array, treat_column_array_as_matrix=True):
        return add_ones(array, treat_column_array_as_matrix)


def create_data_from_text_file(path):
    data = [line.split(',') for line in open(path, 'r').read().splitlines()]
    features = to_array([line[:-1] for line in data], turn_str_items_to_numeric=True)
    results = to_array([line[-1] for line in data], turn_str_items_to_numeric=True)
    return features, results


def add_ones(array, treat_column_array_as_matrix=True):
    if is_matrix(array) and (treat_column_array_as_matrix or isnt_column_array(array)):
        column_of_ones = np.ones(shape=(array.shape[0], 1))
        return np.append(column_of_ones, array, axis=1)
    if len(array.shape) == 1:
        return np.append([1], array)
    return np.append([[1]], array, axis=0)


def verify_has_ones_column(array):
    if is_matrix(array):
        if np.all(array[:, 0] == np.ones(shape=(array.shape[0], 1))):
            return array
        return add_ones(array)

    if len(array.shape) == 1:
        if array[0] == 1:
            return array
        return add_ones(array)

    if array[0][0] == 1:
        return array
    return add_ones(array)


class InputDataFeaturesError(InputError):
    """
    Gets raised when the input_data doesn't have the correct number of features.
    """
    _STRING = "Input data length ({}) should be the same as training data examples length ({})"

    def __init__(self, input_data_row_length, training_data_row_length):
        """
        :param input_data_row_length: The number of features in the new data given
        :type input_data_row_length: int

        :param training_data_row_length: The number of features in the training data
        :type training_data_row_length: int
        """
        super().__init__(self._STRING.format(input_data_row_length, training_data_row_length))


class OptimizationMethodError(YutilsException):
    """
    Gets raised when optimization has failed in scipy.optimize.minimize.
    """
    _STRING = "The optimization method '{method}' raised the error:\n{error}"
    _RECOMMENDATION = "\nYou should try the optimization method '{recommendation}' instead."

    def __init__(self, method, error_message, recommendation=None):
        """
        :param method: The optimization method that raised the error
        :type method: str
        :param error_message: The error message raised during optimization
        :type error_message: str
        :param recommendation: The optimization recommended on using to bypass this error
        :type recommendation: str
        """
        string = self._STRING.format(method=method, error=error_message)
        if recommendation:
            string += self._RECOMMENDATION.format(recommendation=recommendation)
        super().__init__(string)


def get_optimization_info_from_error(error):
    word = '(.*)'
    pattern1 = OptimizationMethodError._STRING.format(method=word, error=word)
    pattern2 = OptimizationMethodError._RECOMMENDATION.format(recommendation=word)

    match = re.search(pattern1, error)
    if not match:
        return

    method, message = match.groups()
    recommendation = None

    match = re.search(pattern2, error)
    if match:
        recommendation, = match.groups()

    return method, message, recommendation
