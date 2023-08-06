#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from abc import ABCMeta, abstractmethod

from yutils.tools.numpy_tools import to_array, r2c, is_matrix
from yutils.ml.base.ml_base import MLObject, verify_has_ones_column, InputDataFeaturesError


class Model(MLObject):
    __metaclass__ = ABCMeta

    _INPUT_DEFAULTS = dict(verbose=True,
                           data_editor=None)

    def __init__(self, training_data, training_results, **kwargs):
        super().__init__(training_data=verify_has_ones_column(to_array(training_data)),
                         training_results=r2c(to_array(training_results)),
                         **kwargs)

        self.training_data = self.training_data  # Purely syntactic, so that the IDE sees that the attribute exists
        self.training_results = self.training_results # Purely syntactic, so that the IDE sees that the attribute exists
        self.m = self.training_results.size
        self.theta = None

        if not hasattr(self, 'data_editor') or not self.data_editor:
            self.data_editor = self._get_default_data_editor()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
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
        pass

    def predict(self, input_data, theta=None):
        """
        Predict an output (or column of outputs) for a given input (or set of input arrays)

        :param input_data: data for prediction
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        :return: prediction
        """
        if theta is None:
            theta = self.theta
        data = self.data_editor(input_data)
        return self._get_predict_result(data, theta)

    @abstractmethod
    def _get_predict_result(self, data, theta):
        pass

    def _get_default_data_editor(self):
        training_data_num_of_features = self.training_data.shape[1]

        def data_editor(data):
            data = to_array(data)
            matrix = is_matrix(data)

            num_of_features = data.shape[1] if matrix else data.size

            if training_data_num_of_features == num_of_features + 1:
                data = self._add_ones(data)
            elif not num_of_features == training_data_num_of_features:
                raise InputDataFeaturesError(num_of_features, training_data_num_of_features)

            return data

        return data_editor

    def plug_in_data_editor(self, data_editor):
        self.data_editor = data_editor
