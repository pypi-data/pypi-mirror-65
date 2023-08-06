#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np
import warnings

from yutils.tools.numpy_tools import r2c, is_matrix, TWO_D_ARRAY_INTS_FLOATS_TYPE
from yutils.ml.models.model import Model


FEATURE_AMOUNT_BORDER = 10000


class NormalEquation(Model):
    REGULARIZATION_LAMBDA = 1

    _INPUT_TYPES = dict(training_data=TWO_D_ARRAY_INTS_FLOATS_TYPE,
                        training_results=TWO_D_ARRAY_INTS_FLOATS_TYPE,
                        assess_for_warning=bool,
                        regularization=bool,
                        regularization_lambda=[int, float],
                        verbose=bool)

    _NONINVERTABILITY_WARNING_MESSAGE = "Non-invertability Warning:\nThis may be a bad use of the Normal Equation.\n" \
                                        "There are too many features in comparison to training examples:\n" \
                                        "# training examples ({data_len}) <= # features ({features})\n" \
                                        "Delete some features or use regularization."
    _CHANGE_METHODS_WARNING = "There are more than {} features, you should use Linear Regression instead."

    def __init__(self, training_data, training_results, assess_for_warning=True, regularization=True,
                 regularization_lambda=REGULARIZATION_LAMBDA, data_editor=False, verbose=True):
        super().__init__(training_data=training_data,
                         training_results=training_results,
                         assess_for_warning=assess_for_warning,
                         regularization=regularization,
                         regularization_lambda=regularization_lambda,
                         data_editor=data_editor,
                         verbose=verbose)

        self.theta = np.zeros(shape=(self.training_data.shape[1], 1))

        self._check_for_warnings(training_data.shape[1])

    def _check_for_warnings(self, num_of_features):
        if not self.assess_for_warning:
            return

        if num_of_features > FEATURE_AMOUNT_BORDER:
            warnings.warn(self._CHANGE_METHODS_WARNING.format(FEATURE_AMOUNT_BORDER))
        if self.m <= num_of_features:
            warnings.warn(self._NONINVERTABILITY_WARNING_MESSAGE.format(data_len=self.m,
                                                                        features=num_of_features))

    def run(self):
        self.theta = np.linalg.pinv(self.training_data.T
                                    @ self.training_data
                                    + self._get_regularization_value()) \
                     @ self.training_data.T \
                     @ self.training_results
        self._verbose_print('Theta:\n' + '\n'.join(map(str, self.theta)))

    def _get_regularization_value(self):
        if not self.regularization:
            return 0

        matrix = np.eye(self.training_data.shape[1])
        matrix[0][0] = 0

        return self.regularization_lambda * matrix

    def _get_predict_result(self, input_data, theta):
        return sum(input_data * theta)[0]

    def get_error(self, inputs, outputs, theta=None):
        """
        Should compute and return the error of the current self.theta hypothesis

        :param inputs: test info (1-column-padded)
        :type inputs: 2-D array
        :param outputs: test results (answers)
        :type outputs: column array
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        """
        if theta is None:
            theta = self.theta
        if not is_matrix(outputs):
            outputs = r2c(outputs)
        inputs = self.data_editor(inputs)

        m = outputs.size
        hypothesis = inputs @ theta
        cost_vector = (hypothesis - outputs) ** 2
        error = (sum(cost_vector)[0]) / (2 * m)

        return error
