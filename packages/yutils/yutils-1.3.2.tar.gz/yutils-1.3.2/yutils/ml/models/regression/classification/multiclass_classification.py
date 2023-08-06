#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

import numpy as np

from yutils.exceptions import WrongInputDatatype
from yutils.tools.numpy_tools import is_matrix, r2c
from yutils.ml.models.model import Model
from yutils.ml.models.regression.classification.classification import Classification
from yutils.ml.models.regression.classification.logistic_regression import LogisticRegression


class MultiClassClassification(Model):
    def __init__(self, training_data, training_results, model=LogisticRegression, **kwargs):
        """
        Executes the one-vs-all in order to classify inputs into multiple classes, using a new hypothesis for each class.

        :param training_data: Data to train algorithm to - columns are features and rows are training examples
                               Column of ones should already be added as first column
        :type training_data: 2-D numpy array

        :param training_results: Results of each training algorithm
        :type training_results: numpy array

        :param model: a Classification model class from yutils.ml.models.regression.classification to optimize the hypothesis for
        :default model: yutils.ml.models.regression.classification.logistic_regression.LogisticRegression
        :type model: yutils.ml.models.regression.classification.Classification
        """
        super().__init__(training_data=training_data, training_results=training_results,
                         model=model, **kwargs)
        if not issubclass(model, Classification):
            raise WrongInputDatatype('model', Classification, type(model))

        self.input_kwargs = kwargs
        self.classification_objects = []
        self.output_classes = np.array([])

    def run(self):
        for result_class in np.unique(self.training_results):
            training_results = np.where(self.training_results == result_class, 1, 0)
            
            # if 'skewed' not in self.input_kwargs:
            #     self.input_kwargs['skewed'] = False
            
            obj = self.model(self.training_data, training_results, **self.input_kwargs)
            obj.run()
            
            self.classification_objects.append(obj)
            self.output_classes = np.append(self.output_classes, result_class)

    def predict(self, input_data, theta=None):
        """
        Predict an output (or column of outputs) for a given input (or set of input arrays)

        :param input_data: data for prediction
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
                        This will override each classification hypothesis's builtin learned theta value.

        :return: prediction, indexes_of_inputs_of_predictions
        """
        num_inputs = input_data.shape[0] if is_matrix(input_data) else 1
        results = np.zeros(shape=(num_inputs, len(self.output_classes)))
        for i, obj in enumerate(self.classification_objects):
            prediction = obj.predict(input_data, theta=theta, return_bool=True)
            results[:, i] = prediction if num_inputs == 1 else prediction[:, 0]

        num_of_answers_per_input = np.apply_along_axis(np.count_nonzero, 1, results)
        indexes_multiple_classes = np.argwhere(num_of_answers_per_input > 1)[:, 0]
        indexes_no_class = np.argwhere(num_of_answers_per_input < 1)[:, 0]

        if indexes_multiple_classes.size:
            self._verbose_print(f'{indexes_multiple_classes.size} inputs had more than one answer')
        if indexes_no_class.size:
            self._verbose_print(f'{indexes_no_class.size} inputs had no answers')

        ignore_indexes = np.append(indexes_multiple_classes, indexes_no_class)
        all_indexes = np.arange(num_inputs)
        successful_results_indexes = all_indexes[np.invert(np.isin(all_indexes, ignore_indexes))]
        successful_class_indexes = np.apply_along_axis(np.argwhere, 1, results[successful_results_indexes])[:, 0]
        classes = self.output_classes[successful_class_indexes]

        return classes, successful_results_indexes

    def _get_predict_result(self, data, theta):
        raise NotImplementedError()

    def get_error(self, inputs, outputs, theta=None):
        """
        Should compute and return the Misclassification Error of all current self.theta hypotheses

        :param inputs: test info (1-column-padded)
        :type inputs: 2-D array
        :param outputs: test results (answers)
        :type outputs: column array
        :param theta: If you wish for a theta different than the current self.theta, you can give it here
        """
        if not is_matrix(outputs):
            outputs = r2c(outputs)

        predictions, successful_indexes = self.predict(inputs, theta=theta)
        num_prediction_failures = inputs.shape[0] - successful_indexes.size

        correspondence = predictions != outputs[successful_indexes]
        return (np.count_nonzero(correspondence) + num_prediction_failures) / correspondence.size
