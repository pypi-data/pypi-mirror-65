#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from types import FunctionType
import numpy as np
from abc import ABCMeta, abstractmethod
import scipy.optimize as spopt

from yutils.tools.numpy_tools import r2c
from yutils.exceptions import DataNotCreatedYet
from yutils.ml.base.ml_base import OptimizationMethodError, get_optimization_info_from_error
from yutils.ml.impl.gradient_checking import GradientChecker
from yutils.ml.impl.plotting.j_cost import plot_j_cost
from yutils.ml.models.model import Model


class Regression(Model):
    __metaclass__ = ABCMeta

    DEFAULT_ITERATIONS = 1000
    DEFAULT_LEARNING_RATE = 0.01    # TODO: check for best learning rate - look at graphs and see which is best
    REGULARIZATION_LAMBDA = 1
    DEFAULT_OPTIMIZATION_METHOD = 'TNC'

    _INPUT_TYPES = dict(verbose=bool,
                        optimizer_verbose=bool,
                        iterations=int,
                        regularization=bool,
                        regularization_lambda=[int, float],
                        use_optimized_gradient_descent=bool,
                        gradient_checking=bool,
                        optimization_method=[type(None), str],
                        data_editor=[type(None), FunctionType],
                        assess_for_warning=bool,
                        learning_rate=float,
                        try_recommended_optimization_methods=bool)

    _INPUT_DEFAULTS = dict(verbose=True,
                           optimizer_verbose=False,
                           iterations=DEFAULT_ITERATIONS,
                           regularization=True,
                           regularization_lambda=REGULARIZATION_LAMBDA,
                           use_optimized_gradient_descent=True,
                           gradient_checking=False,
                           optimization_method=DEFAULT_OPTIMIZATION_METHOD,
                           data_editor=None,
                           assess_for_warning=True,
                           learning_rate=DEFAULT_LEARNING_RATE,
                           try_recommended_optimization_methods=True)

    _MAX_ITERATION_MESSAGES = ['Maximum number of iterations has been exceeded.',
                               'Max. number of function evaluations reached']
    _MAX_ITERATION_REACHED = 'Max iteration ({}) reached.'
    _OPTIMIZATION_MESSAGES_RECOMMENDATIONS = {'Desired error not necessarily achieved due to precision loss.':
                                                  ('BFGS', 'TNC'),
                                              'Linear search failed':
                                                  ('TNC', 'Nelder-Mead')}

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
        super().__init__(training_data=training_data,
                         training_results=training_results,
                         **kwargs)

        # Initialize Variables
        self._j_cost_history = np.array([])
        self._cur_iteration = 0

        self._assess_for_warnings()

    def run(self):
        self._initialize_all_data()
        self._gradient_checking()
        
        if self.use_optimized_gradient_descent:
            self._wrap_run_gradient_descent_optimized()
        else:
            self._run_gradient_descent_self_implementation()

        self._final_print()

    def _final_print(self):
        if self.verbose:
            cost = self._j_cost_history[-1]
            error = self.get_error(self.training_data, self.training_results, self.theta)
            print(f'Final Training Values:    Error - {round(error, 4)} ; Cost - {round(cost, 4)}')

    def _wrap_run_gradient_descent_optimized(self):
        if not self.try_recommended_optimization_methods:
            self._run_gradient_descent_optimized()
            return

        try:
            self._run_gradient_descent_optimized()
        except OptimizationMethodError as e:
            method, message, recommendation = get_optimization_info_from_error(str(e))
            if not recommendation:
                raise
            self._verbose_print(e, color='red')
            self._verbose_print('Trying optimization again with method:', recommendation)
            self.optimization_method = recommendation
            self._wrap_run_gradient_descent_optimized()

    def _run_gradient_descent_optimized(self):
        def _get_cost_and_gradient(theta):
            col_theta = r2c(theta)
            args = (self.training_data, self.training_results, col_theta, self.regularization, self.regularization_lambda)
            return self.compute_cost(*args), self.get_gradient(*args)[:, 0]

        result = spopt.minimize(_get_cost_and_gradient,
                                self.theta[:, 0],
                                method=self.optimization_method,
                                jac=True,
                                callback=self._theta_minimizer_callback_func,
                                options=dict(maxiter=self.iterations, disp=self.optimizer_verbose))

        if not result.success:
            self._manage_optimization_error(result.message)

        self.theta = r2c(result.x)
        self._add_cost()

    def _manage_optimization_error(self, message):
        if message in self._MAX_ITERATION_MESSAGES:
            if self.optimizer_verbose:
                self._verbose_print(self._MAX_ITERATION_REACHED.format(self.iterations))
            return

        known = self._OPTIMIZATION_MESSAGES_RECOMMENDATIONS.get(message)
        if known:
            method, recomm = known
            if method == self.optimization_method:
                raise OptimizationMethodError(method, message, recomm)
        raise OptimizationMethodError(self.optimization_method, message)

    def _run_gradient_descent_self_implementation(self):
        for i in range(0, self.iterations):
            gradient = self.get_gradient(self.training_data, self.training_results, self.theta,
                                         self.regularization, self.regularization_lambda)
            self._gradient_descent_single_step(gradient)
            self._add_cost()

    def _theta_minimizer_callback_func(self, cur_theta):
        self._cur_iteration += 1
        self._add_cost(r2c(cur_theta))

    def _add_cost(self, theta=None):
        if theta is None:
            theta = self.theta
        cost = self.compute_cost(self.training_data, self.training_results, theta, self.regularization,
                                 regularization_lambda=self.regularization_lambda)
        self._j_cost_history = np.append(self._j_cost_history, cost)

    def _initialize_all_data(self):
        self._initialize_theta()

    def _initialize_theta(self):
        self.theta = np.zeros(shape=(self.training_data.shape[1], 1))

    def _gradient_checking(self):
        """
        Compare the _get_gradient function with numerical gradient using two points on the function (epsilon to each side)

        :return: True/False
        """
        if not self.gradient_checking:
            return

        theta_is_array = isinstance(self.theta, np.ndarray)
        x, y, test_theta, architecture = GradientChecker.get_constant_values_to_check(theta_is_array)

        kwargs = dict(regularization=self.regularization,
                      regularization_lambda=self.regularization_lambda)
        if not theta_is_array:
            kwargs['architecture'] = architecture

        def cost_func(theta):
            return self.compute_cost(x, y, theta, **kwargs)

        def gradient_func(theta):
            return self.get_gradient(x, y, theta, **kwargs)

        checker = GradientChecker(cost_func, gradient_func, self.verbose)
        checker.check(test_theta)

    def _gradient_descent_single_step(self, gradient):
        self.theta = self.theta - (self.learning_rate * gradient)

    @classmethod
    def get_gradient(cls, X, y, theta, regularization=True, regularization_lambda=REGULARIZATION_LAMBDA):
        """
        This method should change self.theta.

        :param X: training info (1-column-padded)
        :type X: 2-D array
        :param y: training results (answers)
        :type y: column array
        :param theta: specific prediction to check (current theta)
        :type theta: array
        :param regularization: if gradient should use a regularization term to regularize thetas (except for theta zero)
        :type regularization: bool
        :param regularization_lambda: The size of lambda for the regularization term
                                        By default - is 1.
        :type regularization_lambda: int or float

        :return: gradient for all thetas - an array with a length of all thetas
        :rtype: n + 1 sized array of floats
        """
        theta = r2c(theta)
        if regularization:
            return cls._get_gradient_with_regularization(X, y, theta, regularization_lambda)
        else:
            return cls._get_gradient_without_regularization(X, y, theta)

    @classmethod
    def _get_gradient_with_regularization(cls, X, y, theta, regularization_lambda):
        m = y.size

        theta_zero_summation = (cls._hypothesis(X, theta) - y) * r2c(X[:, 0])
        theta_zero_gradient = (1 / m) * r2c(sum(theta_zero_summation))

        theta_rest_summation = (cls._hypothesis(X, theta) - y) * X[:, 1:]
        theta_rest_regularized_term = (regularization_lambda / m) * theta[1:]
        theta_rest_gradient = ((1 / m) * r2c(sum(theta_rest_summation))) + theta_rest_regularized_term

        gradient = np.append(theta_zero_gradient, theta_rest_gradient, axis=0)

        return gradient

    @classmethod
    def _get_gradient_without_regularization(cls, X, y, theta):
        m = y.size

        summation = (cls._hypothesis(X, theta) - y) * X
        gradient = (1 / m) * r2c(sum(summation))

        return gradient

    @classmethod
    @abstractmethod
    def _hypothesis(cls, X, theta):
        """
        A function that predicts a training result based on training data inputs, and the current theta prediction

        :param X: training info (1-column-padded)
        :type X: 2-D array
        :param theta: specific prediction to check
        :type theta: array

        :return: The hypothesis result
        :rtype: m sized array of floats (m being the amount of training examples - the number of rows in X)
        """
        pass

    @classmethod
    @abstractmethod
    def compute_cost(cls, X, y, theta, regularization=True, regularization_lambda=REGULARIZATION_LAMBDA):
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
        pass

    def _assess_for_warnings(self):
        pass

    def _get_predict_result(self, data, theta):
        return self._hypothesis(data, theta)

    def plot_j_cost(self):
        if not self._j_cost_history.size:
            raise DataNotCreatedYet('run')
        plot_j_cost(self._j_cost_history, model=self)
