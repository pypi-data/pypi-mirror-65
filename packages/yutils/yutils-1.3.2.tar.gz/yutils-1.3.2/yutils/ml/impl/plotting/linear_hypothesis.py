#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np
from matplotlib import pyplot as plt, cm

from yutils.exceptions import InputError
from yutils.tools.numpy_tools import r2c
from yutils.ml.impl.plotting.base import get_model_name


def plot_2feature_hypothesis_linear(trained_model, inputs, outputs, feature_names=('Feature 1', 'Feature 2'), output_label='Results'):
    if inputs.shape[1] != 2:
        raise InputError("Inputs can have only 2 features for 2-feature hypothesis plotting.")
    if len(outputs.shape) != 1:
        if len(outputs.shape) == 2 and outputs.shape[1] == 1:
            outputs = outputs[:, 0]
        else:
            raise InputError("Outputs needs to be a vector or a column vector (matrix with one column).")
    if len(feature_names) != 2:
        raise InputError("There must be 2 feature names.")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_training_data, y_training_data, z_training_data = inputs[:, 0], inputs[:, 1], outputs
    ax.scatter3D(x_training_data, y_training_data, z_training_data)

    xspace = np.linspace(x_training_data.min(), x_training_data.max())
    yspace = np.linspace(y_training_data.min(), y_training_data.max())
    xy_tuples = np.array([[(x, y) for x in xspace] for y in yspace])
    predictions = np.apply_along_axis(trained_model.predict, 2, xy_tuples)
    if len(predictions.shape) == 3 and predictions.shape[2] == 1:
        predictions = predictions[:, :, 0]
    xspace, yspace = np.meshgrid(xspace, yspace)
    ax.plot_surface(xspace, yspace, predictions, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False, edgecolor='none')
    model_name = get_model_name(trained_model)
    plt.suptitle(f'Hypothesis of Trained {model_name}')
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.set_zlabel(output_label)

    plt.show()


def plot_1feature_hypothesis_linear(trained_model, inputs, outputs, feature_name='X', output_label='y'):
    if len(inputs.shape) != 1:
        if len(inputs.shape) == 2 and inputs.shape[1] == 1:
            inputs = inputs[:, 0]
        elif len(inputs.shape) == 2 and inputs.shape[1] > 1:
            raise InputError("Inputs can have only 1 feature for 1-feature hypothesis plotting.")
        else:
            raise InputError("Inputs needs to be a vector or a column vector (matrix with one column).")
    if len(outputs.shape) != 1:
        if len(outputs.shape) == 2 and outputs.shape[1] == 1:
            outputs = outputs[:, 0]
        else:
            raise InputError("Outputs needs to be a vector or a column vector (matrix with one column).")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(inputs, outputs, label='Training Examples', c='r', marker='x')

    additional_range = (inputs.max() - inputs.min()) / 2
    space_min = int(inputs.min() - additional_range)
    space_max = int(inputs.max() + additional_range)
    xspace = np.linspace(space_min, space_max, inputs.size * 3)
    predictions = trained_model.predict(r2c(xspace))[:, 0]
    ax.plot(xspace, predictions, label='Hypothesis')
    model_name = get_model_name(trained_model)
    plt.suptitle(f'Hypothesis of Trained {model_name}')
    ax.set_xlabel(feature_name)
    ax.set_ylabel(output_label)
    ax.legend()
    plt.show()