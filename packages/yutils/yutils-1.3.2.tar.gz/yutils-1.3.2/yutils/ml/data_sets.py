#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np

from yutils.exceptions import CodeMistake, InputError
from yutils.tools import round_half_up
from yutils.tools.numpy_tools import to_array, r2c, is_matrix, TWO_D_ARRAY_INTS_FLOATS_TYPE
from yutils.ml.base.ml_base import MLObject, InputDataFeaturesError
from yutils.ml.impl.features import FeatureNormalizer, AddPolynomialFeatures


class DataSets(MLObject):
    DEFAULT_RATIO = (0.6, 0.2, 0.2)
    NO_DIVISION_RATIO = (1, 0, 0)

    _SET_NAMES = ['Training Set', 'Cross-Validation Set', 'Test Set']

    _INPUT_TYPES = dict(original_training_data=TWO_D_ARRAY_INTS_FLOATS_TYPE,
                        training_results=TWO_D_ARRAY_INTS_FLOATS_TYPE,
                        ratio=(tuple, [float, int]),
                        randomize=bool,
                        normalization=bool,
                        verbose=bool)

    _INPUT_DEFAULTS = dict(ratio=DEFAULT_RATIO,
                           randomize=True,
                           normalization=True,
                           verbose=True)

    def __init__(self, training_data, training_results, **kwargs):
        """
        Divides training data into different sets:
            - Training set (self.training)
            - Cross-Validation set (self.cv)
            - Test set (self.test)
        And also saves their training results (self.training_res, self.cv_res, self.test_res)
        When randomize is set to False, will divide the sets in the order they were given, otherwise will randomize pickings.
        The ratio division is rounded up (in favor of the prior set).

        :param training_data: Data to train algorithm to - columns are features and rows are training examples
        :type training_data: 2-D numpy array

        :param training_results: Results of each training algorithm
        :type training_results: numpy array


            Available keyword arguments:

        :param ratio: The ratio between each set - this is a 3-float/int-item tuple with a sum of 1.
                        The first number is the fraction of training_data/results to assign the *Training Set*
                        The second number is the fraction of training_data/results to assign the *Cross-Validation Set*
                        The third number is the fraction of training_data/results to assign the *Test Set*
        :default ratio: (0.6, 0.2, 0.2) - this means 60% training set, 20% cross-validation set, and 20% test set
        :type ratio: tuple of float/int (len 3)

        :param randomize: When True, will randomize selection of training examples for each group.
                          When False, will divide the training examples in the order they were given.
        :default randomize: True
        :type randomize: bool

        :param normalization: If to normalize the training data (turn them ~ -1 - 1 or ~ -0.5 - 0.5)
                                to make the regression faster and more exact
        :default normalization: True
        :type normalization: bool

        :param verbose: If to print messages
        :default verbose: True
        :type verbose: bool
        """
        super().__init__(original_training_data=to_array(training_data),
                         training_results=r2c(to_array(training_results)),
                         **kwargs)
        self.training_data = self.original_training_data.copy()
        self.training_results = self.training_results # Purely syntactic, so that the IDE sees that the attribute exists

        # Initialize Sets
        self.training = None
        self.cv = None
        self.test = None

        # Initialize Set Results
        self.training_res = None
        self.cv_res = None
        self.test_res = None

        # Initialize Set Metadata
        self.set_sizes = ()
        self.shuffled_indices = np.array([])

        self._training_data_variations = {}

        self._check_inputs()
        self._divide_data_into_sets()

    def _check_inputs(self):
        if sum(self.ratio) != 1:
            raise InputError("The given ratio should be a tuple of floating point numbers, with a sum of 1. (100%)")

    def get_training_set(self, additional_features_max_exponent=1):
        """
        Create a version of self.training set with:
            - An initial column of ones
            - Normalized features
            - Additional polynomial versions of the features
                (if you don't want these, leave additional_features_max_exponent as it's default of 1)

        :param additional_features_max_exponent: Highest exponent of new polynomial features to add
        :default additional_features_max_exponent: 1 (don't create new features, just add a column of ones at the beginning)
        :type additional_features_max_exponent: int

        :return: Tuple of:
                    - Your edited training set
                    - A function that turns new data into the edited data
        :rtype: Tuple, first item: 2-D Numpy Array, second item: function
        """
        result = self._training_data_variations.get(additional_features_max_exponent)
        if result:
            return result

        new_set, func = self._create_set_editor(self.training, additional_features_max_exponent)
        self._training_data_variations[additional_features_max_exponent] = (new_set, func)
        return new_set, func

    def _create_set_editor(self, original_set, exponent=1):
        feature_adder = AddPolynomialFeatures(original_set, exponent)
        new_set = feature_adder.run()

        if self.normalization:
            new_set = new_set.astype(float)  # prevents all values from being -1, 0, or 1 at the end.
            normalizer = FeatureNormalizer(new_set[:, 1:])
            new_set[:, 1:] = normalizer.normalize()

        num_of_features_before_edit = original_set.shape[1]
        num_of_features_after_edit = new_set.shape[1]

        def data_editor(data):
            data = to_array(data)
            matrix = is_matrix(data)
            num_of_features = data.shape[1] if matrix else data.size

            if num_of_features == num_of_features_after_edit:
                return data

            if not num_of_features == num_of_features_before_edit:
                raise InputDataFeaturesError(num_of_features, original_set.shape[1])

            data = feature_adder.use(data)

            if self.normalization:
                data = data.astype(float)  # prevents all values from being -1, 0, or 1 at the end.
                if matrix:
                    data[:, 1:] = normalizer.use(data[:, 1:])
                else:
                    data[1:] = normalizer.use(data[1:])

            return data

        return new_set, data_editor

    def _divide_data_into_sets(self):
        self._create_set_sizes()
        self._shuffle_data()

        self.training = self.training_data[:self.set_sizes[0]]
        self.training_res = self.training_results[:self.set_sizes[0]]

        self.cv = self.training_data[self.set_sizes[0]:self.set_sizes[0] + self.set_sizes[1]]
        self.cv_res = self.training_results[self.set_sizes[0]:self.set_sizes[0] + self.set_sizes[1]]

        self.test = self.training_data[self.set_sizes[0] + self.set_sizes[1]:]
        self.test_res = self.training_results[self.set_sizes[0] + self.set_sizes[1]:]

        if len(self.training) != self.set_sizes[0] \
                or len(self.cv) != self.set_sizes[1] \
                or len(self.test) != self.set_sizes[2]:
            raise CodeMistake("Set sizes slicing is incorrect in DataSets code!")

    def _shuffle_data(self):
        if not self.randomize:
            return

        self.shuffled_indices = np.array(list(range(len(self.training_data))))
        for i in range(3):
            np.random.shuffle(self.shuffled_indices)

        self.training_data = self.training_data[self.shuffled_indices]
        self.training_results = self.training_results[self.shuffled_indices]

    def _create_set_sizes(self):
        m = self.training_results.size
        sizes = []

        for i in self.ratio[:-1]:
            sizes.append(round_half_up(m * i))
        sizes.append(m - sum(sizes))

        self.set_sizes = tuple(sizes)
        self._print_set_sizes()

    def _print_set_sizes(self):
        self._verbose_print("Set sizes will be:")
        self._verbose_print("\t" + "\n\t".join([f"{self._SET_NAMES[i]}: {self.set_sizes[i]}"
                                                for i in range(len(self.set_sizes))]))


def create_data_sets_object_from_precreated_sets(train, train_res, cv, cv_res, test, test_res, verbose=True):
    ds = DataSets(train, train_res, ratio=DataSets.NO_DIVISION_RATIO, randomize=False, verbose=False)
    ds.cv = cv
    ds.cv_res = cv_res
    ds.test = test
    ds.test_res = test_res

    size = train.shape[0] + cv.shape[0] + test.shape[0]
    ds.set_sizes = (train.shape[0], cv.shape[0], test.shape[0])
    ds.ratio = tuple([i / size for i in ds.set_sizes])
    ds.verbose = verbose
    ds._print_set_sizes()
    return ds
