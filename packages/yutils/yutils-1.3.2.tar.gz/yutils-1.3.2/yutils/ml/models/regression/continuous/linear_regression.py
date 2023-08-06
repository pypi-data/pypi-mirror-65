#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import warnings
import numpy as np

from yutils.ml.models.regression.continuous.continuous import Continuous


FEATURE_AMOUNT_BORDER = 10000


class LinearRegression(Continuous):
    _CHANGE_METHODS_WARNING = "There are less than {} features, you should use the Normal Equation instead."

    def _assess_for_warnings(self):
        if self.assess_for_warning and self.training_data.shape[1] < FEATURE_AMOUNT_BORDER:
            warnings.warn(self._CHANGE_METHODS_WARNING.format(FEATURE_AMOUNT_BORDER))

    @classmethod
    def _hypothesis(cls, X, theta):
        return X @ theta

    @classmethod
    def compute_cost(cls, X, y, theta, regularization=True, regularization_lambda=Continuous.REGULARIZATION_LAMBDA):
        """
        Should return the cost of a certain theta prediction

        :param X: training info (1-column-padded)
        :type X: 2-D array
        :param y: training results (answers)
        :type y: column array
        :param theta: specific prediction to check
        :type theta: array
        :param regularization: if cost should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - is 1.
        :type regularization_lambda: int or float

        :return: the cost of the prediction
        :rtype: float
        """
        m = y.size
        hypothesis = X @ theta
        cost_vector = (hypothesis - y) ** 2

        if regularization:
            regularization_term = regularization_lambda * np.sum(theta[1:] ** 2)
        else:
            regularization_term = 0

        j_cost = (np.sum(cost_vector) + regularization_term) / (2 * m)

        return j_cost
