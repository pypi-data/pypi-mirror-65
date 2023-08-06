#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from yutils.tools import get_verbose_printer
from yutils.ml.impl.plotting.base import get_model_name


DEFAULT_LAMBDA_VALUES = tuple([0] + [0.01 * (2 ** i) for i in range(11)])


STRATEGY = """Options to improve hypothesis:
Fixes high variance:
- Get more training examples
- Try smaller sets of features
- Try increasing [regularization] lambda
- Make a smaller NeuralNetwork architecture

Fixes high bias:
- Try getting additional features
- Try adding polynomial features
- Try decreasing [regularization] lambda
- Add neurons to NeuralNetwork (more neurons in hidden layer, or more hidden layers)
"""


def plot_learning_curve(training_set, training_results, cross_validation_set, cross_validation_results, model,
                        num_of_randomizations=1, max_set_size=50, randomize=True, lc_verbose=True, **model_kwargs):
    """
    Plots learning curves in order to understand if model is suffering from high bias or high variance.

    Models with high bias are attributed with both high training error and high cross-validation error,
        as the number of examples used goes up.
    Models with high variance are attributed with both LOW training error and high cross-validation error,
        as the number of examples used goes up.
        This is because the high variance trains itself to the intricacies of the training data,
        even if it doesn't generalize well to the cross-validation set.

    :param training_set: Inputs for training hypotheses (1-column-padded)
    :type training_set: 2D ndarray

    :param training_results: Results / expected outputs for training the hypotheses
    :type training_results: 2D column ndarray

    :param cross_validation_set: Inputs for testing hypotheses (1-column-padded)
    :type cross_validation_set: 2D ndarray

    :param cross_validation_results: Results / expected outputs for testing the hypotheses
    :type cross_validation_results: 2D column ndarray

    :param model: a Regression model class to train (non-instanced)
    :type model: models that inherit from yutils.ml.models.regression.regression.Regression class

    :param num_of_randomizations: The number of hypotheses to train on each number of training examples.
                                    The error will be averaged across the different hypotheses created.
                                  A higher number should be used to prevent statistical fluctuations more likely
                                    in small datasets.
                                  There is no need to bring this number above 50.
    :default num_of_randomizations: 1 (no new randomizations)
    :type num_of_randomizations: int

    :param max_set_size: The maximum number of training examples to use. Set this maximum if your set size is very big.
    :default max_set_size: 50
    :type max_set_size: int

    :param randomize: If to randomize picking of training examples out of the given sets
    :default randomize: True
    :type randomize: bool

    :param lc_verbose: Learning Curve verbose - if to print messages throughout the execution of this function
    :default lc_verbose: True
    :type lc_verbose: bool

    :param model_kwargs: All keyword arguments you wish to input into your model at instance creation, for training.
    """
    if not randomize:
        num_of_randomizations = 1
    vprint = get_verbose_printer(lc_verbose)

    m_train = training_set.shape[0]
    max_num_of_examples = min(max_set_size, m_train)

    error_train = np.zeros(max_num_of_examples)
    error_cv = np.zeros(max_num_of_examples)

    for i in range(1, max_num_of_examples + 1):
        vprint(f'Training hypothesis for i={i} examples')
        for randomization in range(num_of_randomizations):
            i_err_train = []
            i_err_cv = []

            if randomize:
                training_indices = np.random.permutation(np.arange(m_train))[:i]
            else:
                training_indices = np.arange(i)

            i_rand_train = training_set[training_indices]
            i_rand_train_res = training_results[training_indices]

            hypothesis = model(i_rand_train, i_rand_train_res, **model_kwargs)
            hypothesis.run()

            i_err_train.append(hypothesis.get_error(i_rand_train, i_rand_train_res))
            i_err_cv.append(hypothesis.get_error(cross_validation_set, cross_validation_results))

        error_train[i - 1] = np.average(i_err_train)
        error_cv[i - 1] = np.average(i_err_cv)

    example_number = np.arange(1, max_num_of_examples + 1)
    errors = pd.DataFrame(np.array([error_train, error_cv]).T)
    errors.index = example_number
    errors.index.name = 'Num of Examples'
    errors.columns = ['Training Error', 'Cross Validation Error']
    vprint(errors)

    plt.plot(example_number, error_train, label='Training Error')
    plt.plot(example_number, error_cv, label='Cross Validation Error')
    model_name = get_model_name(model)
    plt.suptitle(f'Learning curve for {model_name}')
    plt.xlabel('Number of training examples')
    plt.ylabel('Error')
    plt.legend()
    plt.show()


def plot_validation_curve(training_set, training_results, cross_validation_set, cross_validation_results, model,
                          lambda_options=DEFAULT_LAMBDA_VALUES, lc_verbose=True, **model_kwargs):
    """
    Plots validation curves in order to see the influence of different regularization lambda values.

    :param training_set: Inputs for training hypotheses (1-column-padded)
    :type training_set: 2D ndarray

    :param training_results: Results / expected outputs for training the hypotheses
    :type training_results: 2D column ndarray

    :param cross_validation_set: Inputs for testing hypotheses (1-column-padded)
    :type cross_validation_set: 2D ndarray

    :param cross_validation_results: Results / expected outputs for testing the hypotheses
    :type cross_validation_results: 2D column ndarray

    :param model: a Regression model class to train (non-instanced)
    :type model: models that inherit from yutils.ml.models.regression.regression.Regression class

    :param lambda_options: A list of options for lambda values, to iterate over and train the model with.
    :default lambda_options: (0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24)
    :type lambda_options: list of (ints or floats)

    :param lc_verbose: Learning Curve verbose - if to print messages throughout the execution of this function
    :default lc_verbose: True
    :type lc_verbose: bool

    :param model_kwargs: All keyword arguments you wish to input into your model at instance creation, for training.
    """
    vprint = get_verbose_printer(lc_verbose)

    error_train = np.zeros(len(lambda_options))
    error_cv = np.zeros(len(lambda_options))

    for i, option in enumerate(lambda_options):
        vprint(f'Training hypothesis for lambda={option}')

        model_kwargs['regularization'] = True
        model_kwargs['regularization_lambda'] = option
        hypothesis = model(training_set, training_results, **model_kwargs)
        hypothesis.run()

        error_train[i] = hypothesis.get_error(training_set, training_results)
        error_cv[i] = hypothesis.get_error(cross_validation_set, cross_validation_results)

    errors = pd.DataFrame(np.array([error_train, error_cv]).T)
    errors.index = lambda_options
    errors.index.name = 'Lambda Options'
    errors.columns = ['Training Error', 'Cross Validation Error']
    vprint(errors)

    plt.plot(lambda_options, error_train, label='Training Error')
    plt.plot(lambda_options, error_cv, label='Cross Validation Error')
    model_name = get_model_name(model)
    plt.suptitle(f'Validation curve for {model_name}')
    plt.xlabel('Regularization Lambda')
    plt.ylabel('Error')
    plt.legend()
    plt.show()


def print_strategy():
    print(STRATEGY)
