#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.ml.data_sets import DataSets, create_data_sets_object_from_precreated_sets
from yutils.ml.base.ml_base import create_data_from_text_file, add_ones
from yutils.ml.impl.features import FeatureNormalizer, AddPolynomialFeatures
from yutils.ml.impl.plotting.curves import plot_learning_curve, plot_validation_curve, print_strategy
from yutils.ml.models.regression.continuous.linear_regression import LinearRegression
from yutils.ml.models.regression.classification.logistic_regression import LogisticRegression
from yutils.ml.models.regression.classification.neural_network import NeuralNetwork
from yutils.ml.models.regression.classification.multiclass_classification import MultiClassClassification
from yutils.ml.models.others.continuous.normal_equation import NormalEquation
from yutils.ml.ml_optimizer import MLOptimizer


# TODO: add normalization of y if range of y is extremely large, multiple orders of magnitude.
# TODO: have different options of MLOptimizer inputs: max_degree, degree_options, max_lambda, lambda_options, threshold, different architectures, etc.
# TODO: add ability in MLOptimizer to change Model kwargs inputs based on option currently training (e.g. change nn_archetecture based on degree of polynomial)
