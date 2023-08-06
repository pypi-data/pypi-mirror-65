#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from functools import reduce
import numpy as np

from yutils.exceptions import CodeMistake
from yutils.tools.numpy_tools import r2c
from yutils.ml.base.ml_base import MLObject


class GradientChecker(MLObject):
    EPSILON = 10 ** -4
    ARRAY_ARCHITECTURE = 3
    MULTI_LAYER_ARCHITECTURE = (3, 5, 3)
    NUM_TRAINING_EXAMPLES = 5

    def __init__(self, cost_func, gradient_func, verbose=True):
        """
        Checks to see if the gradient computation is correct. Useful for debugging Regression algorithms.

        :param cost_func: function that receives a theta value and returns the cost of theta.
        :type cost_func: function
        :param gradient_func: function that receives a theta value and returns the gradients of theta.
        :type gradient_func: function
        """
        self.cost_func = cost_func
        self.gradient_func = gradient_func
        self.verbose = verbose

    @staticmethod
    def _get_constant_values_matrix(fan_out, fan_in):
        return np.reshape(np.sin(np.arange(fan_out * (fan_in + 1))), (fan_out, fan_in + 1))

    @classmethod
    def get_constant_values_to_check(cls, theta_is_array=True):
        if theta_is_array:
            architecture = cls.ARRAY_ARCHITECTURE
            theta = cls._get_constant_values_matrix(architecture + 1)
            x = cls._add_ones(cls._get_constant_values_matrix(cls.NUM_TRAINING_EXAMPLES,
                                                              architecture))
            y = r2c(1 + np.mod(np.arange(cls.NUM_TRAINING_EXAMPLES), 2))
        else:
            architecture = cls.MULTI_LAYER_ARCHITECTURE
            theta = cls._roll([cls._get_constant_values_matrix(architecture[i + 1],
                                                               architecture[i])
                               for i in range(len(architecture) - 1)])
            x = cls._add_ones(cls._get_constant_values_matrix(cls.NUM_TRAINING_EXAMPLES,
                                                              architecture[0] - 1))
            y = r2c(1 + np.mod(np.arange(cls.NUM_TRAINING_EXAMPLES), architecture[-1]))

        return x, y, theta, architecture

    @staticmethod
    def _roll(lst_of_arrays):
        return reduce(np.append, lst_of_arrays)

    def check(self, theta):
        numerical_gradient = np.zeros(theta.size)
        perturb = np.zeros(theta.size)
        for p in range(theta.size):
            perturb[p] = self.EPSILON
            loss1 = self.cost_func(theta - perturb)
            loss2 = self.cost_func(theta + perturb)
            numerical_gradient[p] = (loss2 - loss1) / (2 * self.EPSILON)
            perturb[p] = 0

        analytical_gradient = self._roll(self.gradient_func(theta))
        similarity = self._check_array_similarity(analytical_gradient, numerical_gradient)

        self._verbose_print('Gradient Checking similarity value (analytic vs numerical gradient:', similarity)

        if not similarity < 10 ** -9:
            raise CodeMistake("Analytical Gradient and Numerical Gradient aren't similar:\n"
                              f"Similarity {similarity} >= 10 ** -9")

    @staticmethod
    def _check_array_similarity(array1, array2):
        return np.linalg.norm(array1 - array2) / np.linalg.norm(array1 + array2)
