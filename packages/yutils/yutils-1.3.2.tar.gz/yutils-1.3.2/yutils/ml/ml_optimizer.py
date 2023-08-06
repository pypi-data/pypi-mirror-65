#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import datetime
import time
import math
import decimal
from decimal import Decimal
decimal.setcontext(decimal.BasicContext)
from types import FunctionType
from inspect import signature

from yutils.exceptions import WrongInputDatatype, InputError, NoDataError
from yutils.tools import dict_of_options_to_subdicts
from yutils.ml.base.ml_base import MLObject, OptimizationMethodError
from yutils.ml.data_sets import DataSets
from yutils.ml.models.model import Model


class MLOptimizer(MLObject):
    DEFAULT_MAX_LAMBDA = 10.24
    DEFAULT_ADDITIONAL_FEATURES_MAX_EXPONENT = 5
    DEFAULT_THRESHOLD_PRECISION = 0.2
    HIGH_THRESHOLD_PRECISION = 0.1

    _INPUT_TYPES = dict(data_sets=[type(None), DataSets],
                        max_degree=int,
                        max_lambda=[int, float],
                        include_lambda_zero=bool,
                        verbose=bool)

    _INPUT_DEFAULTS = dict(max_degree=DEFAULT_ADDITIONAL_FEATURES_MAX_EXPONENT,
                           max_lambda=DEFAULT_MAX_LAMBDA,
                           include_lambda_zero=True,
                           verbose=True)

    _SPECIAL_KWARGS = ['max_lambda', 'threshold_precision', 'include_lambda_zero', 'verbose']

    _TRAINING_ERROR = "!!! Error while training model '{ident}' !!!\n{error_type}: {error_message}"

    def __init__(self, data_sets=None, max_degree=DEFAULT_ADDITIONAL_FEATURES_MAX_EXPONENT, **kwargs):
        """
        Finds the best possible hypothesis for a specific type of ML model.

        :param data_sets: optional DataSets object you have created with training/cross-validation/test sets defined
        :type data_sets: yutils.ml.data_sets.DataSets object

        :param max_degree: The highest polynomial exponent of additional features you wish to add.
                           A list of options will be created, from 1 to the number given
                                Each value will be trained on with the training set,
                                and the error will be computed on the cross-validation set.
                                The degree with the lowest cross-validation error will be chosen
                                for the final hypothesis.
        :default max_degree: 1 -> (DEFAULT_ADDITIONAL_FEATURES_MAX_EXPONENT) : Currently 1-5
        :type max_degree: int


        :param **kwargs:

                * * * * * * * * * * * *
            Here you can also add more variables to loop over when creating new trained hypotheses.
            Any given variable should be a list of values to give the model.
            For example:
                threshold=[0.1, 0.3, 0.5, 0.7, 0.9]
                This will create 5 versions of each hypothesis, giving threshold the first value in the list,
                    then the second, etc.
                * * * * * * * * * * * *



            *SPECIAL* kwargs you can also give:

        :param max_lambda: The highest lambda regularization value you wish to train with.
                            This is an alternative, easier way to create a list of regularization_lambda options.
                           A list of options will be created, beginning with 0 and exponentially going up to your number.
                                Each value will be trained on with the training set,
                                and the error will be computed on the cross-validation set.
                                The lambda value with the lowest cross-validation error will be chosen
                                for the final hypothesis.
        :default max_lambda: 10.24  This will create:
                            (0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24)
        :type max_lambda: int or float


        :param degree: A list of options for polynomial exponents for additional features you wish to add.
                                    This is an alternative to using max_degree (which gives a list of 1-max_degree as options)
                                    Each value will be trained on with the training set,
                                    and the error will be computed on the cross-validation set.
                                    The degree with the lowest cross-validation error will be chosen
                                    for the final hypothesis.
        :default degree: (0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24)
        :type degree: list of ints

        :param threshold_precision: The precision of threshold values to try.
                            This is an alternative, easier way to create a list of threshold options.
                            This precision must be bigger than 0 and smaller than 0.5.
                           A list of options will be created, beginning with 0.5 and looping outwards (up and down)
                           by the given precision.

                           For example, a precision of 0.1 will give 0.1, 0.2, .... 0.8, 0.9
                           A precision of 0.2 will give 0.1, 0.3, 0.5, 0.7, 0.9

                                Each value will be trained on with the training set,
                                and the error will be computed on the cross-validation set.
                                The threshold with the lowest cross-validation error
                                (if classes are skewed, this will be the f-score) will be chosen
                                for the final hypothesis.
        :type threshold_precision: float

        :param include_lambda_zero: Whether or not to include regularization_lambda=0 in list of
                                        automatically created lambda values
        :default include_lambda_zero: True
        :type include_lambda_zero: bool

        :param verbose: If to print messages
        :default verbose: True
        :type verbose: bool
        """
        super().__init__(data_sets=data_sets, max_degree=max_degree, **kwargs)
        self.kwargs_for_hypotheses = self._check_and_edit_kwargs(kwargs)

        self._trained_hypotheses = {}
        self._model_class = None
        self._training_kwargs = {}
        self._conditional_training_kwargs = {}
        self._cv_values = {}
        self.final_hypothesis = None
        self._kwargs_abbreviations = self._get_kwargs_abbreviations()

    def _check_and_edit_kwargs(self, kwargs):
        kwargs_for_hypotheses = {}

        for arg, value in kwargs.items():
            if arg not in self._SPECIAL_KWARGS:
                if not isinstance(value, (list, tuple)):
                    raise WrongInputDatatype(arg, list, type(value))
                kwargs_for_hypotheses[arg] = value

        if 'degree' not in kwargs:
            self.degree = list(range(1, self.max_degree + 1))
            kwargs_for_hypotheses['degree'] = self.degree
        if 'regularization_lambda' not in kwargs:
            self.regularization_lambda = self._get_lambda_options()
            kwargs_for_hypotheses['regularization_lambda'] = self.regularization_lambda
        if 'threshold' not in kwargs and 'threshold_precision' in kwargs:
            self.threshold = self._get_thresholds()
            kwargs_for_hypotheses['threshold'] = self.threshold

        return kwargs_for_hypotheses

    def _get_lambda_options(self):
        num_of_nonzero_vals = int(math.log2(self.max_lambda * 100)) + 1
        lambda_options = [(2 ** i) / 100 for i in range(num_of_nonzero_vals)]
        if self.include_lambda_zero:
            lambda_options = [0] + lambda_options
        if self.max_lambda not in lambda_options:
            lambda_options.append(self.max_lambda)
        return lambda_options

    def _get_thresholds(self):
        precision = self.threshold_precision
        if precision > 0.5 or precision < 0:
            raise InputError('Argument threshold_precision must be between 0 and 0.5')
        base = Decimal((0, (5,), -1))
        precision_digits = tuple(map(int, str(precision).replace('0.', '')))
        precision = Decimal((0, precision_digits, -len(precision_digits)))
        thresholds = [base]
        jumps = int(base / precision)
        for direction in (1, -1):
            for i in range(jumps):
                thresholds.append(base + precision * (i + 1) * direction)
        if 0.0 in thresholds:
            thresholds.remove(0.0)
            thresholds.remove(1.0)
        thresholds.sort()
        thresholds = list(map(float, thresholds))
        return thresholds

    def _get_kwargs_abbreviations(self):
        keys = list(self.kwargs_for_hypotheses.keys())
        keys.sort()
        abbreviations = []
        for key in keys:
            abbr = ''.join(word[0].upper() for word in key.split('_'))

            # If abbreviation exists
            i = 1
            while abbr in abbreviations:
                abbr = ''.join(word[:i].capitalize() for word in key.split('_'))
                i += 1

            abbreviations.append(abbr)
        return dict(zip(keys, abbreviations))

    def create_data(self, training_data, training_results, **kwargs):
        if 'verbose' not in kwargs:
            kwargs['verbose'] = self.verbose
        self.data_sets = DataSets(training_data, training_results, **kwargs)

    create_data.__doc__ = DataSets.__init__.__doc__

    def run(self, model_class, conditional_args=(), **kwargs):
        """
        Will optimize the hypothesis for the given model class.

        :param model_class: a Model class from yutils.ml.models to optimize the hypothesis for
        :type model_class: yutils.ml.models.model.Model (usually yutils.ml.models.regression.Regression)

        :param conditional_args: A list of argument names in kwargs that should be set according to conditions met
                                (see below)
        :type conditional_args: list/tuple of strings


        :param kwargs: KeyWord Arguments you wish to give as __init__ keywords to your class.

                * * * * * * * * * * * *
          Conditional keyword arguments:

            Should be 2-item-long tuple of format: (input/s, function)

            The second item is a function that returns the desired argument value
            The first item is the name of the looped-over argument to give to the function as input.
                This can be a string, or a tuple of strings (for multiple inputs to your second-item function)
                You can give argument names like 'threshold' and 'regularization_lambda',
                and you can also give the special argument 'degree' to reference the degree of polynomial
                for the new features created for the training_data given.

            If you have given conditional keyword arguments,
            don't forget to put their names under the conditional_args argument.

            Example usages, in order to get the NeuralNetwork Architecture for neural networks in the optimizer loop:

                nn_architecture=('degree', lambda degree: disperse_length(degree, 3))

                or:

                def get_architecture(degree):
                    if degree == 1:
                        return (4, 5, 1)
                    if degree == 2:
                        return (10, 7, 1)
                    if degree == 3:
                        return (20, 10, 1)
                nn_architecture=('degree', get_architecture)

                * * * * * * * * * * * *


        :return: a class instance of the chosen model_class type, with an optimized hypothesis
        :rtype: model_class
        """
        if not issubclass(model_class, Model):
            raise WrongInputDatatype('model_class', Model, type(model_class))
        if not (self.data_sets.cv.size and self.data_sets.test.size):
            raise InputError('MLOptimizer must have non-empty Cross-Validation and Test sets.')
        self._model_class = model_class
        self._training_kwargs, self._conditional_training_kwargs = self._check_training_kwargs(conditional_args, kwargs)

        self._iter_vars_and_train_all()

        self.final_hypothesis = self._choose_hypothesis_using_cv()

        error = self.final_hypothesis.get_error(self.data_sets.test, self.data_sets.test_res)
        self._verbose_print("Final test set error:", error)

        return self.final_hypothesis

    def _check_training_kwargs(self, conditional_args, kwargs):
        conditional_kwargs = {}
        for arg in conditional_args:
            value = kwargs.pop(arg)
            if isinstance(value[0], str):
                value = ((value[0],), value[1])
            self._check_conditional_arg(arg, value)
            conditional_kwargs[arg] = value
        return kwargs, conditional_kwargs

    def _check_conditional_arg(self, name, tup):
        inputs, func = tup

        if not (isinstance(func, FunctionType) and isinstance(inputs, (list, tuple))):
            raise InputError(f'Conditional argument {name} has incorrect format. Review self.run() docstring for help.')

        num_params = len(signature(func).parameters)
        if num_params != len(inputs):
            raise InputError(f'Conditional argument {name} has {len(inputs)} arguments as inputs, '
                             f'but func has {num_params} inputs')

        for inp in inputs:
            if inp not in list(self.kwargs_for_hypotheses):
                raise InputError(f'Conditional argument {name} has input {inp} '
                                 f'not given as loop kwarg in __init__.')

    def _iter_vars_and_train_all(self):
        kwargs_dicts = dict_of_options_to_subdicts(self.kwargs_for_hypotheses)
        num_of_trained_models = len(kwargs_dicts)
        self._verbose_print(f"Beginning training of {num_of_trained_models} models...")

        counter = 0
        for kwargs_dict in kwargs_dicts:
            training_set, func = self.data_sets.get_training_set(kwargs_dict['degree'])
            ident = ';'.join(f'{self._kwargs_abbreviations[key]}:{value}'
                             for key, value in kwargs_dict.items())
            counter += 1
            cur_time = datetime.datetime.fromtimestamp(time.time())
            self._verbose_print(f"Training model #{counter}: '{ident}'   - {cur_time}")

            try:
                self._train_model(training_set, self.data_sets.training_res, ident, data_editor=func, **kwargs_dict)
            except OptimizationMethodError as e:
                self._verbose_print(self._TRAINING_ERROR.format(ident=ident,
                                                                error_type=type(e).__name__,
                                                                error_message=e),
                                    color='red')

    def _train_model(self, training_data, training_results, dict_identifier, **new_kwargs):
        kwargs = {}
        kwargs.update(self._training_kwargs)
        kwargs.update(new_kwargs)
        kwargs.update(self._get_conditional_kwargs(kwargs))

        if 'verbose' not in kwargs:
            kwargs['verbose'] = self.verbose

        instance = self._model_class(training_data, training_results, **kwargs)
        instance.run()

        self._trained_hypotheses[dict_identifier] = instance

    def _get_conditional_kwargs(self, kwargs):
        conditional_kwargs = {}
        for arg, condition in self._conditional_training_kwargs.items():
            inputs_names, func = condition
            inputs = [kwargs[name] for name in inputs_names]
            conditional_kwargs[arg] = func(*inputs)
        return conditional_kwargs

    def _choose_hypothesis_using_cv(self):
        if not self._trained_hypotheses:
            raise NoDataError('No model hypotheses created yet.')

        for ident, hyp in self._trained_hypotheses.items():
            self._cv_values[ident] = hyp.get_error(self.data_sets.cv, self.data_sets.cv_res)

        cv_error_sizes = list(self._cv_values.values())
        lowest_cv_error, amount, average, highest = min(cv_error_sizes), len(cv_error_sizes), \
                                                    sum(cv_error_sizes) / len(cv_error_sizes), max(cv_error_sizes)
        self._verbose_print(f'\n{amount} hypotheses created.\n'
                            f'Min Error: {lowest_cv_error}\n'
                            f'Max Error: {highest}\n'
                            f'Avg Error: {average}')
        chosen_identifiers = [ident for ident, val in self._cv_values.items() if val == lowest_cv_error]

        if len(chosen_identifiers) > 1:
            self._verbose_print("More than one hypotheses with lowest CV error found:")
            self._verbose_print(chosen_identifiers)
            self._verbose_print(f"Picking first in list: {chosen_identifiers[0]}")

        ident = chosen_identifiers[0]
        self._verbose_print(f"Hypothesis {ident} found with CV error of {self._cv_values[ident]}")
        return self._trained_hypotheses[ident]




