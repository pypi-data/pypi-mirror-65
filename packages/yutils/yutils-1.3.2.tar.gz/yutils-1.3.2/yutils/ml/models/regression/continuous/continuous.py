#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.tools.numpy_tools import r2c, is_matrix
from yutils.ml.models.regression.regression import Regression
from yutils.ml.impl.plotting.linear_hypothesis import plot_2feature_hypothesis_linear, plot_1feature_hypothesis_linear


class Continuous(Regression):
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
        return self.compute_cost(inputs, outputs, theta, regularization=False)

    def plot_2feature_hypothesis(self, inputs=None, outputs=None, feature_names=('Feature 1', 'Feature 2'), output_label='Results'):
        inputs = self.training_data[:, 1:] if inputs is None else inputs
        outputs = self.training_results if outputs is None else outputs

        plot_2feature_hypothesis_linear(self, inputs, outputs, feature_names=feature_names, output_label=output_label)

    def plot_1feature_hypothesis(self, inputs=None, outputs=None, feature_name='X', output_label='y'):
        inputs = self.training_data[:, 1:] if inputs is None else inputs
        outputs = self.training_results if outputs is None else outputs

        plot_1feature_hypothesis_linear(self, inputs, outputs, feature_name=feature_name, output_label=output_label)
