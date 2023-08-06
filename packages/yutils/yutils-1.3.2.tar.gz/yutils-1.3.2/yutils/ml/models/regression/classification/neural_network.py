#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import time, datetime
from functools import reduce
import scipy.optimize as spopt
import numpy as np

from yutils.tools import istype
from yutils.exceptions import InputError
from yutils.tools.numpy_tools import r2c, is_matrix, isnt_column_array
from yutils.ml.models.regression.classification.classification import Classification


GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


class NeuralNetwork(Classification):
    DEFAULT_ITERATIONS = 50
    DEFAULT_NUM_HIDDEN_LAYERS = 1
    DEFAULT_OPTIMIZATION_METHOD = 'CG'

    _OPTIMIZATION_METHOD_THETA_LENGTH_BOUNDARY = 500

    _NEURALNETWORK_EXTRA_INPUT_TYPES = dict(only_count_iterations=bool,
                                            nn_architecture=(tuple, int),
                                            num_hidden_layers=int,
                                            hidden_layers_size=[type(None), int])

    _NEURALNETWORK_EXTRA_INPUT_DEFAULTS = dict(only_count_iterations=True,
                                               nn_architecture=(),
                                               num_hidden_layers=DEFAULT_NUM_HIDDEN_LAYERS,
                                               hidden_layers_size=None)

    def __init__(self, training_data, training_results, **kwargs):
        """
        Creates a regression object, for use in linearization/classification problems.

        :param training_data: Data to train algorithm to - columns are features and rows are training examples
        :type training_data: 2-D numpy array
        :param training_results: Results of each training algorithm
        :type training_results: numpy array

        :param kwargs: Additional keyword arguments


            Available keyword arguments:

        :param nn_architecture: The amount of nodes/units in every layer of the Neural Network
                                (including the input layer, output layer, and all hidden layers.
        :default nn_architecture: Will create a (num_hidden_layers + 2)-layer Neural Network:
                                  default: (input_layer_size, hidden_layer_size, output_layer_size)
                                        input_layer_size: length of training_data row
                                        hidden_layer_size: int(input_layer_size * golden_ratio)
                                        output_layer_size: amount of output classes defined in training_results
                                  raising the number of num_hidden_layers creates more hidden_layers of the same size.
        :type nn_architecture: tuple of ints

        :param num_hidden_layers: To be used instead of nn_architecture - to easily create a Neural Network
                                    with more than one hidden layer
                                  The amount of units in each layer will be the same, and defined as:
                                        hidden_layer_size: int(input_layer_size * golden_ratio)
        :default num_hidden_layers: cls.DEFAULT_NUM_HIDDEN_LAYERS
        :type num_hidden_layers: int

        :param hidden_layers_size: The amount of nodes/units in each hidden layer (defined by num_hiddel_layers).
                                    If you wish to give a different size to each layer, use nn_architecture instead.
        :default hidden_layers_size: When defaulted to None, is computed as the number of input nodes/units * the golden ratio.
        :type hidden_layers_size: int

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

        :param gradient_checking: If to check the gradient function against a numerical gradient, to debug
        :default gradient_checking: False
        :type gradient_checking: bool

        :param optimization_method: Name of scipy.optimize.minimize optimization method to use for minimization of
                                    cost function.
                                    Will be ignored if use_optimized_gradient_descent is False.
                                    Reccommendation: "TNC" (Truncated Newton method) for regression with few theta values,
                                                     "CG" (Conjugate Gradient) for regression with huge theta value matrices
                                                     "BFGS" is another option for short thetas, but sometimes raises warnings
        :default optimization_method: By default (None) will use the default scipy.optimize.minimize (usually BFGS)
        :type optimization_method: str

        :param data_editor: A function that receives new data and edits it in the same way the original data was edited
                                before being given to this class.
                            Usually, this function adds new features that need to be added (e.g. polynomial features)
                                and performs normalization on all columns based on the original data's 'sigma' and 'mu'.
        :default data_editor: None
        :type data_editor: function

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

        :param only_count_iterations: Instead of optimizer_verbose being on, with cost and error messages for every iteration,
                                        Only iteration count (on same line with "\r" carriage return) will be printed.
                                      This helps the user understand the stage the execution is currently on.
        :default only_count_iterations: True
        :type only_count_iterations: bool
        """
        self._INPUT_TYPES.update(self._NEURALNETWORK_EXTRA_INPUT_TYPES)
        self._INPUT_DEFAULTS.update(self._NEURALNETWORK_EXTRA_INPUT_DEFAULTS)

        super().__init__(training_data, training_results, **kwargs)
        
        self.num_input_units = self.training_data.shape[1] - 1  # Because inputs now have an extra column of ones
        self.output_classes, self.num_output_classes = self._get_num_output_classes()
        self.original_training_results, self.training_results = self.training_results, self._get_new_training_results()
        self._check_inputs()
        self._create_nn_architecture()
        
        self._layer_outputs_a = [None] * len(self.nn_architecture)
        self._layer_inputs_z = [None] * len(self.nn_architecture)

    def _check_inputs(self):
        if self.nn_architecture:
            if not self.nn_architecture[0] == self.num_input_units:
                raise InputError("Input 'nn_architecture' first item should be the length of training_data row")

            if not self.nn_architecture[-1] == self.num_output_classes:
                raise InputError("Input 'nn_architecture' last item should be the number of training_results labels")

    def _get_num_output_classes(self):
        classes = np.unique(self.training_results[:, 0])
        classes.sort()
        num = len(classes)
        if num == 2:
            num = 1
        return classes, num

    def _get_new_training_results(self):
        if self.num_output_classes == 1:
            return self.output_classes[1] == self.training_results
        return self.output_classes == self.training_results

    def _create_nn_architecture(self):
        if not self.nn_architecture:
            if not self.hidden_layers_size:
                self.hidden_layers_size = int(self.num_input_units * GOLDEN_RATIO)
            self.nn_architecture = (self.num_input_units,) + \
                                   (self.hidden_layers_size,) * self.num_hidden_layers + \
                                   (self.num_output_classes,)

    def _initialize_theta(self):
        self.theta = [self._rand_initialize_weights(from_layer, self.nn_architecture[from_layer_index + 1])
                      for from_layer_index, from_layer in enumerate(self.nn_architecture[:-1])]

    @staticmethod
    def _rand_initialize_weights(layer_size_in, layer_size_out):
        """
        Returns a random initialization of weights in the range of -epsion to +epsilon
        Epsilon will be sqrt(6) / sqrt(layer_size_in + layer_size_out)

        :param layer_size_in: number of units in the layer adjacent to Theta(l) (before it)
        :type layer_size_in: int
        :param layer_size_out: number of units in the layer adjacent to Theta(l) (after it)
        :type layer_size_out: int

        :return: Random weights (array of size layer_size_in by (layer_size_out + 1)
        :rtype: numpy.ndarray
        """
        epsilon_init = round((6 ** 0.5) / ((layer_size_in + layer_size_out) ** 0.5), 4)
        return np.random.random((layer_size_out, layer_size_in + 1)) * 2 * epsilon_init - epsilon_init

    def _final_print(self):
        if self.verbose:
            cost = self._j_cost_history[-1]
            error = self.get_error(self.training_data, self.original_training_results, self.theta)
            print(f'Final Training Values:    Error - {round(error, 4)} ; Cost - {round(cost, 4)}')

    def _hypothesis(self, X, theta, bias_unit_already_added=True):
        if not bias_unit_already_added:
            X = self._add_ones(X)

        if is_matrix(X) and isnt_column_array(X):
            return self._feedforward(X, theta, lambda a, thet: a @ thet.T)
        return self._feedforward(r2c(X), theta, lambda a, thet: thet @ a)

    def _feedforward(self, X, theta, matrix_mult_func):
        # What this actually does:
        # arr = X
        # for i in range(len(self.nn_architecture) - 1):
        #     if i != 0:
        #         arr = self._add_ones(arr, False)
        #     arr = self._sigmoid(matrix_mult_func(arr, theta[i]))
        # return arr
        # But we need to save the answers of the feedforward algorithm for later use in self.get_gradient

        self._layer_outputs_a[0] = X
        for layer_index in range(len(self.nn_architecture) - 1):
            if layer_index != 0:
                self._layer_outputs_a[layer_index] = self._add_ones(self._layer_outputs_a[layer_index], False)
            self._layer_inputs_z[layer_index + 1] = matrix_mult_func(self._layer_outputs_a[layer_index],
                                                                     theta[layer_index])
            self._layer_outputs_a[layer_index + 1] = self._sigmoid(self._layer_inputs_z[layer_index + 1])
        return self._layer_outputs_a[-1]

    @staticmethod
    def _sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @classmethod
    def _sigmoid_gradient(cls, z):
        return cls._sigmoid(z) * (1 - cls._sigmoid(z))

    def compute_cost(self, X, y, theta, regularization=True, architecture=None, regularization_lambda=None, **kwargs):
        """
        Should return the cost of a certain theta prediction

        :param X: training info (1-column-padded)
        :type X: 2-D array
        :param y: training results (answers)
        :type y: column array
        :param theta: list of weights for each layer of network (current theta)
        :type theta: list of 2-D arrays, or 1-D array that function will unravel
        :param regularization: if cost should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param architecture: The number of units in each layer of your Neural Network architecture
                                Left blank this will default to self.nn_architecture
        :type architecture: tuple of ints
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - None, will use self.regularization_lambda
        :type regularization_lambda: int or float

        :return: the cost of the prediction
        :rtype: float
        """
        regularization_lambda = self.regularization_lambda if regularization_lambda is None else regularization_lambda
        architecture = self.nn_architecture if architecture is None else architecture
        theta = theta if istype(theta, (list, np.ndarray)) else self._unroll(theta, architecture=architecture)
        m = y.shape[0]

        y_true_computation = (-1 * y) * np.log(self._hypothesis(X, theta))
        y_false_computation = (1 - y) * np.log(1 - self._hypothesis(X, theta))

        if regularization:
            regularization_term = (regularization_lambda / (2 * m)) * sum(sum(sum(t[:, 1:] ** 2)) for t in theta)
        else:
            regularization_term = 0

        j_cost_no_reg = (1 / m) * sum(sum(y_true_computation - y_false_computation))
        j_cost = j_cost_no_reg + regularization_term
        return j_cost

    def get_gradient(self, X, y, theta, regularization=True, architecture=None, regularization_lambda=None):
        """
        This method should change self.theta.

        :param X: training info (1-column-padded)
        :type X: 2-D array
        :param y: training results (answers)
        :type y: 2-D array
        :param theta: list of weights for each layer of network (current theta)
        :type theta: list of 2-D arrays, or 1-D array that function will unravel
        :param regularization: if gradient should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param architecture: The number of units in each layer of your Neural Network architecture
                                Left blank this will default to self.nn_architecture
        :type architecture: tuple of ints
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - None, will use self.regularization_lambda
        :type regularization_lambda: int or float

        :return: gradient for all thetas - an array with a length of all thetas - rolled out to single 1-D array
        :rtype: list of numpy.ndarrays
        """
        regularization_lambda = self.regularization_lambda if regularization_lambda is None else regularization_lambda
        architecture = self.nn_architecture if architecture is None else architecture
        theta = theta if istype(theta, (list, np.ndarray)) else self._unroll(theta, architecture=architecture)
        m = y.shape[0]
        final_delta = [np.zeros(shape=t.shape) for t in theta]
        gradient = [np.zeros(shape=t.shape) for t in theta]
        
        for i in range(m):
            hypothesis = self._hypothesis(X[i], theta)
            delta = [None] * len(self.nn_architecture)
            delta[-1] = hypothesis - r2c(y[i])
            for l in range(len(self.nn_architecture) - 2, 0, -1):
                delta[l] = (theta[l][:, 1:].T @ delta[l + 1]) * self._sigmoid_gradient(self._layer_inputs_z[l])
            for l in range(len(final_delta)):
                final_delta[l] = final_delta[l] + (delta[l + 1] * self._layer_outputs_a[l].T)

        for l in range(len(gradient)):
            gradient[l] = (1 / m) * final_delta[l]

        if regularization:
            for l in range(len(gradient)):
                gradient[l][:, 1:] = gradient[l][:, 1:] + ((regularization_lambda / m) * theta[l][:, 1:])

        return gradient

    def _unroll(self, array, architecture=None):
        architecture = self.nn_architecture if architecture is None else architecture
        output = []
        index = 0
        for l in range(len(architecture) - 1):
            in_layer, out_layer = architecture[l], architecture[l + 1]
            length = (in_layer + 1) * out_layer
            output.append(np.reshape(array[index:index + length], (out_layer, in_layer + 1)))
            index += length
        return output

    @staticmethod
    def _roll(lst_of_arrays):
        return reduce(np.append, lst_of_arrays)

    def _theta_minimizer_callback_func(self, cur_theta):
        theta = self._unroll(cur_theta)
        self._cur_iteration += 1
        self._add_cost(theta)
        if self.optimizer_verbose:
            cost = self._j_cost_history[-1]
            error = self.get_error(self.training_data, self.original_training_results, theta) * 100
            self._verbose_print(f'Beginning Iteration: {self._cur_iteration}',
                                f' ~ Error: {round(error, 3)}%',
                                f' ~ Cost Function Value: {round(cost, 4)}',
                                f' ~ Time: {datetime.datetime.fromtimestamp(time.time())}')
        elif self.only_count_iterations and self.verbose:
            print(f'\rIteration: {self._cur_iteration}/{self.iterations}', end='')

    def _choose_optimization_method(self):
        if 'optimization_method' in self._inputs_without_defaults:
            return
        if sum(t.size for t in self.theta) > self._OPTIMIZATION_METHOD_THETA_LENGTH_BOUNDARY:
            self.optimization_method = 'CG'
            self._verbose_print('Changed optimization method to "CG", because theta has many values.')

    def _run_gradient_descent_optimized(self):
        self._choose_optimization_method()

        def _get_cost_and_gradient(theta):
            return self.compute_cost(self.training_data, self.training_results, theta, self.regularization), \
                   self._roll(self.get_gradient(self.training_data, self.training_results, theta, self.regularization))

        result = spopt.minimize(_get_cost_and_gradient,
                                self._roll(self.theta),
                                method=self.optimization_method,
                                jac=True,
                                callback=self._theta_minimizer_callback_func,
                                options=dict(maxiter=self.iterations, disp=self.optimizer_verbose))

        if self.only_count_iterations:
            self._verbose_print('')
        
        if not result.success:
            self._manage_optimization_error(result.message)

        self.theta = self._unroll(result.x)
        self._add_cost()

    def predict(self, input_data, theta=None, **kwargs):
        predictions = super().predict(input_data, theta, return_bool=self.num_output_classes == 1)
        if is_matrix(predictions) and isnt_column_array(predictions):
            indexes = r2c(np.argmax(predictions, axis=1))
        elif self.num_output_classes == 1:
            indexes = predictions.astype(int)
        else:
            indexes = r2c(np.argmax(predictions))
        return self.output_classes[indexes]
