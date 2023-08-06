#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.neighbors import NearestNeighbors

from yutils.exceptions import InputError
from yutils.ml.impl.plotting.base import get_model_name


def plot_3feature_decision_boundary(trained_model, inputs, outputs, class_names=None,
                                    feature_names=('Feature 1', 'Feature 2', 'Feature 3'), precision=50):
    if inputs.shape[1] != 3:
        raise InputError("Inputs must have 3 features for 3-feature hypothesis plotting.")
    if len(outputs.shape) != 1:
        if len(outputs.shape) == 2 and outputs.shape[1] == 1:
            outputs = outputs[:, 0]
        else:
            raise InputError("Outputs needs to be a vector or a column vector (matrix with one column).")
    classes = tuple(np.unique(outputs))
    class_names = tuple(map(str, class_names)) if class_names else classes
    if len(classes) > 2:
        raise InputError("Outputs have more than 2 classes. Only 2 are allowed.")
    elif len(classes) < 2:
        raise InputError("Outputs must have 2 classes.")
    if len(class_names) != 2:
        raise InputError("There must be 2 class names.")
    if len(feature_names) != 3:
        raise InputError("There must be 3 feature names.")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_training_data_0, y_training_data_0, z_training_data_0 = inputs[outputs == classes[0], 0], \
                                                              inputs[outputs == classes[0], 1], \
                                                              inputs[outputs == classes[0], 2]
    x_training_data_1, y_training_data_1, z_training_data_1 = inputs[outputs == classes[1], 0], \
                                                              inputs[outputs == classes[1], 1], \
                                                              inputs[outputs == classes[1], 2]
    ax.scatter3D(x_training_data_0, y_training_data_0, z_training_data_0,
                 marker='o', c='y', edgecolors='k', label=class_names[0])
    ax.scatter3D(x_training_data_1, y_training_data_1, z_training_data_1,
                 marker='+', label=class_names[1])

    all_x, all_y, all_z = inputs[:, 0], inputs[:, 1], inputs[:, 2]

    xspace = np.linspace(all_x.min() - 2, all_x.max() + 2, precision)
    yspace = np.linspace(all_y.min() - 2, all_y.max() + 2, precision)
    zspace = np.linspace(all_z.min() - 2, all_z.max() + 2, precision)

    xyz_tuples = np.array([[[(x, y, z) for x in xspace] for y in yspace] for z in zspace])
    predictions = np.apply_along_axis(trained_model.predict, 3, xyz_tuples)
    if len(predictions.shape) == 4 and predictions.shape[3] == 1:
        predictions = predictions[:, :, :, 0]

    to_false, to_true = get_true_false_borders_in_cube(predictions)

    xspace, yspace, zspace = np.meshgrid(xspace, yspace, zspace)
    x_to_true, x_to_false = xspace[to_true], xspace[to_false]
    y_to_true, y_to_false = yspace[to_true], yspace[to_false]
    z_to_true, z_to_false = zspace[to_true], zspace[to_false]

    x_boundary, y_boundary, z_boundary = find_middle_points_3d(x_to_true, y_to_true, z_to_true,
                                                               x_to_false, y_to_false, z_to_false)

    ax.scatter3D(x_boundary, y_boundary, z_boundary,
                 marker='.', c='r', label='Decision Boundary')
    # surf = ax.plot_trisurf(x_boundary, y_boundary, z_boundary, label='Decision Boundary')
    # surf._facecolors2d = surf._facecolors3d  # to fix bug in matplotlib that hasn't been fixed yet
    # surf._edgecolors2d = surf._edgecolors3d  # to fix bug in matplotlib that hasn't been fixed yet

    model_name = get_model_name(trained_model)
    plt.suptitle(f'Decision Boundary for {model_name}')
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.set_zlabel(feature_names[2])
    plt.legend()
    plt.show()


def plot_2feature_decision_boundary(trained_model, inputs, outputs, class_names=None,
                                    feature_names=('Feature 1', 'Feature 2'), precision=200):
    if inputs.shape[1] != 2:
        raise InputError("Inputs must have 2 features for 2-feature hypothesis plotting.")
    if len(outputs.shape) != 1:
        if len(outputs.shape) == 2 and outputs.shape[1] == 1:
            outputs = outputs[:, 0]
        else:
            raise InputError("Outputs needs to be a vector or a column vector (matrix with one column).")
    classes = tuple(np.unique(outputs))
    class_names = tuple(map(str, class_names)) if class_names else classes
    if len(classes) > 2:
        raise InputError("Outputs have more than 2 classes. Only 2 are allowed.")
    elif len(classes) < 2:
        raise InputError("Outputs must have 2 classes.")
    if len(class_names) != 2:
        raise InputError("There must be 2 class names.")
    if len(feature_names) != 2:
        raise InputError("There must be 2 feature names.")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x_training_data_0, y_training_data_0, = inputs[outputs == classes[0], 0], inputs[outputs == classes[0], 1]
    x_training_data_1, y_training_data_1, = inputs[outputs == classes[1], 0], inputs[outputs == classes[1], 1]
    ax.scatter(x_training_data_0, y_training_data_0, marker='o', c='y', edgecolors='k', label=class_names[0])
    ax.scatter(x_training_data_1, y_training_data_1, marker='+', label=class_names[1])

    all_x, all_y = inputs[:, 0], inputs[:, 1]
    x_additional_range = (all_x.max() - all_x.min()) / 8
    y_additional_range = (all_y.max() - all_y.min()) / 8

    xspace = np.linspace(all_x.min() - x_additional_range, all_x.max() + y_additional_range, precision)
    yspace = np.linspace(all_y.min() - y_additional_range, all_y.max() + y_additional_range, precision)
    xy_tuples = np.array([[(x, y) for x in xspace] for y in yspace])

    predictions = np.apply_along_axis(trained_model.predict, 2, xy_tuples)
    
    if len(predictions.shape) == 3 and predictions.shape[2] == 1:
        predictions = predictions[:, :, 0]
    elif len(predictions.shape) == 4 and predictions.shape[2] == 1 and predictions.shape[3] == 1:
        predictions = predictions[:, :, 0, 0]

    to_false, to_true = get_true_false_borders_in_square(predictions)
    xspace, yspace = np.meshgrid(xspace, yspace)
    x_to_true, x_to_false = xspace[to_true], xspace[to_false]
    y_to_true, y_to_false = yspace[to_true], yspace[to_false]

    x_boundary, y_boundary = find_middle_points_2d(x_to_true, y_to_true, x_to_false, y_to_false)

    ax.scatter(x_boundary, y_boundary, s=13, marker='.', c='r', label='Decision Boundary')
    #ax.plot(x_boundary, y_boundary, label='Decision Boundary')

    model_name = get_model_name(trained_model)
    plt.suptitle(f'Decision Boundary for {model_name}')
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.legend(bbox_to_anchor=(1.02, 0.5), loc='center left', ncol=1, fancybox=True, shadow=True)
    #fig.tight_layout()
    fig.subplots_adjust(right=0.75)
    plt.show()


def get_true_false_borders_in_cube(cube):
    right_f = np.append(cube[1:, :, :], np.ones(shape=(1, cube.shape[1], cube.shape[2])).astype(bool), axis=0) == False
    left_f = np.append(np.ones(shape=(1, cube.shape[1], cube.shape[2])).astype(bool), cube[:-1, :, :], axis=0) == False
    forward_f = np.append(cube[:, 1:, :], np.ones(shape=(cube.shape[0], 1, cube.shape[2])).astype(bool), axis=1) == False
    backward_f = np.append(np.ones(shape=(cube.shape[0], 1, cube.shape[2])).astype(bool), cube[:, :-1, :], axis=1) == False
    up_f = np.append(cube[:, :, 1:], np.ones(shape=(cube.shape[0], cube.shape[1], 1)).astype(bool), axis=2) == False
    down_f = np.append(np.ones(shape=(cube.shape[0], cube.shape[1], 1)).astype(bool), cube[:, :, :-1], axis=2) == False

    true_near_false = np.logical_and(cube == True,
                                     np.logical_or(right_f,
                                                   np.logical_or(left_f,
                                                                 np.logical_or(forward_f,
                                                                               np.logical_or(backward_f,
                                                                                             np.logical_or(up_f,
                                                                                                           down_f))))))

    right_t = np.append(cube[1:, :, :], np.zeros(shape=(1, cube.shape[1], cube.shape[2])).astype(bool), axis=0) == True
    left_t = np.append(np.zeros(shape=(1, cube.shape[1], cube.shape[2])).astype(bool), cube[:-1, :, :], axis=0) == True
    forward_t = np.append(cube[:, 1:, :], np.zeros(shape=(cube.shape[0], 1, cube.shape[2])).astype(bool), axis=1) == True
    backward_t = np.append(np.zeros(shape=(cube.shape[0], 1, cube.shape[2])).astype(bool), cube[:, :-1, :], axis=1) == True
    up_t = np.append(cube[:, :, 1:], np.zeros(shape=(cube.shape[0], cube.shape[1], 1)).astype(bool), axis=2) == True
    down_t = np.append(np.zeros(shape=(cube.shape[0], cube.shape[1], 1)).astype(bool), cube[:, :, :-1], axis=2) == True

    false_near_true = np.logical_and(cube == False,
                                     np.logical_or(right_t,
                                                   np.logical_or(left_t,
                                                                 np.logical_or(forward_t,
                                                                               np.logical_or(backward_t,
                                                                                             np.logical_or(up_t,
                                                                                                           down_t))))))

    return true_near_false, false_near_true


def get_true_false_borders_in_square(square):
    right_f = np.append(square[1:, :], np.ones(shape=(1, square.shape[1])).astype(bool), axis=0) == False
    left_f = np.append(np.ones(shape=(1, square.shape[1])).astype(bool), square[:-1, :], axis=0) == False
    forward_f = np.append(square[:, 1:], np.ones(shape=(square.shape[0], 1)).astype(bool), axis=1) == False
    backward_f = np.append(np.ones(shape=(square.shape[0], 1)).astype(bool), square[:, :-1], axis=1) == False

    true_near_false = np.logical_and(square == True,
                                     np.logical_or(right_f,
                                                   np.logical_or(left_f,
                                                                 np.logical_or(forward_f, backward_f))))

    right_t = np.append(square[1:, :], np.zeros(shape=(1, square.shape[1])).astype(bool), axis=0) == True
    left_t = np.append(np.zeros(shape=(1, square.shape[1])).astype(bool), square[:-1, :], axis=0) == True
    forward_t = np.append(square[:, 1:], np.zeros(shape=(square.shape[0], 1)).astype(bool), axis=1) == True
    backward_t = np.append(np.zeros(shape=(square.shape[0], 1)).astype(bool), square[:, :-1], axis=1) == True

    false_near_true = np.logical_and(square == False,
                                     np.logical_or(right_t,
                                                   np.logical_or(left_t,
                                                                 np.logical_or(forward_t, backward_t))))

    return true_near_false, false_near_true


def find_middle_points_3d(x_first, y_first, z_first, x_second, y_second, z_second):
    dots_first = np.array([x_first, y_first, z_first]).T
    dots_second = np.array([x_second, y_second, z_second]).T

    neighbor_finder = NearestNeighbors(n_neighbors=1).fit(dots_first)
    indices = neighbor_finder.kneighbors(dots_second, return_distance=False)

    new_x = (x_first[indices[:, 0]] + x_second) / 2
    new_y = (y_first[indices[:, 0]] + y_second) / 2
    new_z = (y_first[indices[:, 0]] + z_second) / 2
    return new_x, new_y, new_z


def find_middle_points_2d(x_first, y_first, x_second, y_second):
    dots_first = np.array([x_first, y_first]).T
    dots_second = np.array([x_second, y_second]).T

    neighbor_finder = NearestNeighbors(n_neighbors=1).fit(dots_first)
    indices = neighbor_finder.kneighbors(dots_second, return_distance=False)

    new_x = (x_first[indices[:, 0]] + x_second) / 2
    new_y = (y_first[indices[:, 0]] + y_second) / 2
    return new_x, new_y
