#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np

from yutils.tools.itertools import disperse
from yutils.tools.numpy_tools import is_matrix, normalize_array, TWO_D_NP_ARRAY_INTS_FLOATS_TYPE
from yutils.ml.base.ml_base import MLObject


class FeatureNormalizer(MLObject):
    _INPUT_TYPES = dict(original_info=TWO_D_NP_ARRAY_INTS_FLOATS_TYPE)

    def __init__(self, info):
        """
        Normalizes features for a ML object

        :param info: info to normalize, across column axis (normalizes each column by different normalization data)
        :type info:
        """
        super().__init__(original_info=info, info=info)
        self.mu = np.zeros(shape=(info.shape[1], 1))  # average values
        self.sigma = np.ones(shape=(info.shape[1], 1))  # Standard Deviation values

    def normalize(self):
        self.info, self.mu, self.sigma = normalize_array(self.original_info, axis=0)
        return self.info

    def use(self, array):
        return (array - self.mu) / self.sigma


class AddPolynomialFeatures(MLObject):
    _INPUT_TYPES = dict(original_info=TWO_D_NP_ARRAY_INTS_FLOATS_TYPE)

    MAX_EXPONENT = 6

    def __init__(self, info, max_exponent=MAX_EXPONENT):
        """
        Adds more features to a set of column features -
        All polynomial versions of the features up to the add_powers_up_to power.

        For example, for a set of features x1 and x2, with add_powers_up_to being 2, you will receive the features:
        x1, x2, x1^2, x2^2, x1x2, x1^2*x2, x1*x2^2, x1^2*x2^2

        :param info: features to add polynomial versions of (across column axis)
        :type info: array of arrays of ints/floats
        :param max_exponent: the highest power to add a feature version of
        :type max_exponent: int
        """
        super().__init__(original_info=info, max_exponent=max_exponent)
        self._num_of_original_features = info.shape[1]
        self.powers_order = np.eye(self._num_of_original_features)
        self.info = None

    def run(self):
        self.powers_order = self._get_powers()
        self.info = self.use(self.original_info)
        return self.info

    def use(self, data):
        if is_matrix(data):
            return np.vstack([self._create_polynomial_feature(data, features_power) for features_power in self.powers_order]).T
        return self._create_polynomial_feature(data, self.powers_order)

    def _get_powers(self):
        powers = disperse(self.max_exponent, self._num_of_original_features)
        powers.sort(key=self._order_key)
        return np.array(powers)

    @staticmethod
    def _order_key(item):
        order = [max(item), sum(item)] + [-i for i in item]
        return tuple(order)

    def _create_polynomial_feature(self, data, powers):
        return np.product(np.power(data, powers), axis=1)
