#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np

from yutils.tools.numpy_tools import r2c
from yutils.ml.models.regression.classification.classification import Classification


class LogisticRegression(Classification):
    @classmethod
    def _hypothesis(cls, X, theta):
        return cls._sigmoid(X @ theta)

    @staticmethod
    def _sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @classmethod
    def compute_cost(cls, X, y, theta, regularization=True, regularization_lambda=Classification.REGULARIZATION_LAMBDA):
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
        theta = r2c(theta)
        m = y.size

        y_true_computation = (y.T @ np.log(cls._hypothesis(X, theta)))[0][0]
        y_false_computation = ((1 - y).T @ np.log(1 - cls._hypothesis(X, theta)))[0][0]


        if regularization:
            regularization_term = (regularization_lambda / (2 * m)) * sum(theta[1:] ** 2)[0]
        else:
            regularization_term = 0

        j_cost_no_reg = (1 / m) * (-y_true_computation - y_false_computation)
        j_cost = j_cost_no_reg + regularization_term
        return j_cost
