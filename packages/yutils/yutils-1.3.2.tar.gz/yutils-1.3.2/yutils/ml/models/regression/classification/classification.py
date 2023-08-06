#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import warnings
import numpy as np

from yutils.exceptions import YutilsException
from yutils.tools.numpy_tools import r2c, is_matrix
from yutils.ml.models.regression.regression import Regression
from yutils.ml.impl.plotting.plot_decision_boundary import plot_2feature_decision_boundary, plot_3feature_decision_boundary


class Classification(Regression):
    DEFAULT_THRESHOLD = 0.5
    SKEWED_THRESHOLD = 0.15  # Classes will be considered "skewed" if less than 15% of them are ones
    _OPPOSITE_SKEWED_CLASSES_WARNING = "Classes are skewed, but usually the rare class ({}) is tagged as 1, " \
                                       "and the other as 0. Consider editing your training results."

    _CLASSIFICATION_EXTRA_INPUT_TYPES = dict(threshold=float,
                                             skewed=[type(None), bool])

    _CLASSIFICATION_EXTRA_INPUT_DEFAULTS = dict(threshold=DEFAULT_THRESHOLD,
                                                skewed=None)

    def __init__(self, training_data, training_results, **kwargs):
        """
        Creates a regression object, for use in linearization/classification problems.

        :param training_data: Data to train algorithm to - columns are features and rows are training examples
                                Column of ones should already be added as first column
        :type training_data: 2-D numpy array
        :param training_results: Results of each training algorithm
        :type training_results: numpy array

        :param kwargs: Additional keyword arguments


            Available keyword arguments:

        :param iterations: Number of iterations to descend
        :default iterations: cls.DEFAULT_ITERATIONS
        :type iterations: int

        :param regularization: If to regularize the gradient descent, in order to prevent overfitting of the training data.
                                This means to penalize, or "tax" the growth of theta values of features.
                                This prevents theta values of irrelevant features from growing.
        :default regularization: True
        :type regularization: bool

        :param regularization_lambda: The weight to give the regularization term for regularized gradient descent.
                                      This is the weight of the penalization, or "tax" on the grown of theta values of features.
                                        A bigger value will prevent overfitting in that it prevents theta values for
                                        irrelevant features from growing. Too big a value, though can create underfitting.
        :default regularization_lambda: 1
        :type regularization_lambda: int or float

        :param threshold: The threshold on which to classify if the prediction is a yes (1) or a no (0)
                            By default is 0.5
                            Give a higher threshold for less false positives, give a lower threshold for less false negatives.
        :default threshold: 0.5
        :type threshold: float

        :param skewed: If the data is skewed (if there are many more of one class of training data than there are of the other class
        :type skewed: bool

        :param use_optimized_gradient_descent: If you would rather use a more advanced optimizer (scipy.optimize.minimize)
                                                to run gradient descent, than a self-created implementation here
        :default use_optimized_gradient_descent: True
        :type use_optimized_gradient_descent: bool

        :param gradient_checking: If to check the gradient function against a numerical gradient, to debug
        :default gradient_checking: False
        :type gradient_checking: bool

        :param optimization_method: Name of scipy.optimize.minimize optimization method to use for minimization of
                                    cost function.
                                    Will be ignored if use_optimized_gradient_descent is False.
                                    Reccommendation: "TNC" (Truncated Newton method) for regression with few theta values,
                                                     "CG" (Conjugate Gradient) for regression with huge theta value matrices
                                                     "BFGS" is another option for short thetas, but sometimes raises warnings
        :default optimization_method: default or None will use the default scipy.optimize.minimize (usually BFGS)
        :type optimization_method: str

        :param data_editor: A function that receives new data and edits it in the same way the original data was edited
                                before being given to this class.
                            Usually, this function adds new features that need to be added (e.g. polynomial features)
                                and performs normalization on all columns based on the original data's 'sigma' and 'mu'.
        :default data_editor: None
        :type data_editor: function

        :param assess_for_warning: If to raise warnings if they emerge
        :default assess_for_warning: True
        :type assess_for_warning: bool

        :param learning_rate: Alpha Coefficient for managing descent speed
                                This is relevant only if use_optimized_gradient_descent is set to False
                                (optimization will be done manually)
        :default learning_rate: cls.DEFAULT_LEARNING_RATE
        :type learning_rate: float

        :param try_recommended_optimization_methods: If scipy.optimize.minimize raises a known error,
                                                        and I can recommend a new optimization method instead,
                                                        try it automatically.
        :default try_recommended_optimization_methods: True
        :type try_recommended_optimization_methods: bool

        :param verbose: If to print messages
        :default verbose: True
        :type verbose: bool

        :param optimizer_verbose: If the scipy optimizer/minimizer should print it's builtin optimization messages
        :default optimizer_verbose: False
        :type optimizer_verbose: bool
        """
        self._INPUT_TYPES.update(self._CLASSIFICATION_EXTRA_INPUT_TYPES)
        self._INPUT_DEFAULTS.update(self._CLASSIFICATION_EXTRA_INPUT_DEFAULTS)
        super().__init__(training_data=training_data,
                         training_results=training_results,
                         **kwargs)
        self.skewed, self._skewed_rare_class = self._check_if_classes_are_skewed(self.skewed)

    def _check_if_classes_are_skewed(self, skewed=None):
        if skewed is False:
            return False, None

        classes, counts = np.unique(self.training_results, return_counts=True)
        least_amount, least_amt_index = np.min(counts), np.argmin(counts)
        rare_class = classes[least_amt_index]
        ratio = least_amount / self.training_results.size

        if skewed is True:
            return True, rare_class

        if len(classes) != 2 or ratio > self.SKEWED_THRESHOLD:
            return False, None

        self._verbose_print(f"Classes have been defined as skewed (ratio is {round(ratio, 4)}. "
                            f"Least common class: {rare_class}")

        if self.assess_for_warning and rare_class != 1:
            warnings.warn(self._OPPOSITE_SKEWED_CLASSES_WARNING.format(rare_class))

        return True, rare_class

    def predict(self, input_data, theta=None, return_bool=True):
        """
        Predict an output (or column of outputs) for a given input (or set of input arrays)

        :param input_data: data for prediction
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        :param return_bool: If is False, will return level of certainty.
                            If is True, will return True/False as a prediction (if level of certainty is above self.threshold)
        :return: prediction
        """
        predictions = super().predict(input_data, theta=theta)
        if return_bool:
            return predictions > self.threshold
        return predictions

    def get_error(self, inputs, outputs, theta=None):
        """
        Should compute and return the Misclassification Error of the current self.theta hypothesis

        :param inputs: test info (1-column-padded)
        :type inputs: 2-D array
        :param outputs: test results (answers)
        :type outputs: column array
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        """
        if self.skewed:
            return self.get_f_score(inputs, outputs, theta=theta)

        if not is_matrix(outputs):
            outputs = r2c(outputs)

        predictions = self.predict(inputs, theta=theta, return_bool=True)
        correspondence = predictions != outputs
        return np.mean(correspondence)

    def get_f_score(self, inputs, outputs, theta=None):
        """
        Should compute and return the F1-Score of the current hypothesis (taking into account precision and recall)
        This is used for hypotheses with skewed classes.

        :param inputs: test info (1-column-padded)
        :type inputs: 2-D array
        :param outputs: test results (answers)
        :type outputs: column array
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        """
        if not self.skewed:
            raise ClassesArentSkewed()

        if not is_matrix(outputs):
            outputs = r2c(outputs)

        predictions = self.predict(inputs, theta=theta, return_bool=True)

        true_positives = np.count_nonzero(np.logical_and(predictions == self._skewed_rare_class,
                                                         outputs == self._skewed_rare_class))
        predicted_positives = np.count_nonzero(predictions == self._skewed_rare_class)
        actual_positives = np.count_nonzero(outputs == self._skewed_rare_class)

        precision = true_positives / predicted_positives
        recall = true_positives / actual_positives

        f_score = 2 * (precision * recall) / (precision + recall)
        return f_score

    def plot_2feature_hypothesis(self, inputs=None, outputs=None, class_names=None,
                                 feature_names=('Feature 1', 'Feature 2'), precision=200):
        inputs = self.training_data[:, 1:] if inputs is None else inputs
        outputs = self.training_results if outputs is None else outputs

        plot_2feature_decision_boundary(self, inputs, outputs,
                                        class_names=class_names, feature_names=feature_names, precision=precision)

    def plot_3feature_hypothesis(self, inputs=None, outputs=None, class_names=None,
                                 feature_names=('Feature 1', 'Feature 2', 'Feature 3'), precision=50):
        inputs = self.training_data[:, 1:] if inputs is None else inputs
        outputs = self.training_results if outputs is None else outputs

        plot_3feature_decision_boundary(self, inputs, outputs,
                                        class_names=class_names, feature_names=feature_names, precision=precision)


class ClassesArentSkewed(YutilsException):
    """
    Gets raised when the user is looking for information that is used for skewed classes.
    """
    _STRING = "Classes in training_results aren't skewed, this information is irrelevant. " \
              "If you wish to use it, give skewed=True to __init__ (sets self.skewed as True)"

    def __init__(self):
        super().__init__(self._STRING)
