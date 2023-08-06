# -*- coding: utf-8 -*-
""""""  # for sphinx auto doc purposes
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from LNNS 1.0 A neural network simulator [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
|
| This file is part of the QGIS Neural Network MLP Classifier plugin and mlp-image-classifier python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License along with Foobar.  If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, cohen_kappa_score
from sklearn.model_selection import train_test_split


class Network:
    """
    The Network class create a neural network using the sklearn.neural_network.MLPClassifier.
    The network can be used to predict classified images using supervised classification.
    """

    def __init__(self, number_of_hidden, activation):
        """
        The number of input and number of output neurons are not required for MLPClassifier. It  extracts this
        information from the training data set.

        :param Tuple[int] number_of_hidden: Number of hidden neurons, multiple layers are possible (see Tuple notation)
        :param activation: str Activation function for the MLPClassifier. Possible values are
            'identity', 'logistic', 'tanh', 'relu'
        """
        self.number_of_hidden = number_of_hidden
        self.network = MLPClassifier(hidden_layer_sizes=number_of_hidden, random_state=100,
                                     activation=activation, learning_rate_init=0.1, learning_rate='constant',
                                     momentum=0, tol=0)
        self.validation_results = None
        self.unique_classes = None

    def validate(self, x_test, y_test, log_function=print):
        """
        The trained neural network can be evaluated using a test set of the data. The validation results will be saved
        in the validation_results dictionary with the keys: Average accuracy, a Kappa for each predicted class,
        an average kappa and a rapport including precision, recall, f1-score and support.

        Example output:

        .. line-block::

            Average accuracy: 0.9740708729472775
            Kappa class 1: 0.9996048676750681
            Kappa class 2: 0.9969686283161031
            Kappa class 3: 0.9269671354418852
            Kappa class 4: 0.9384942730689072
            Kappa class 5: 0.9854574554108237
            Kappa class 6: 0.8991142021469177
            Average Kappa: 0.9577677603432843


        =========== ========= ====== ========  =======
        .           precision recall f1-score  support
        =========== ========= ====== ========  =======
                  0  1.00      1.00   1.00      1664
                  1  1.00      1.00   1.00       956
                  2  0.91      0.96   0.93       597
                  3  0.96      0.94   0.95      1149
                  4  1.00      0.98   0.99      2345
                  5  0.88      0.92   0.90       231

        avg / total  0.98      0.98   0.98      6942
        =========== ========= ====== ========  =======

        :param ndarray[float] x_test: test input variables
        :param ndarray[float] y_test: test output values
        :param log_function: function to log
        """

        self.validation_results = {'average_accuracy': self.network.score(x_test, y_test)}
        log_function("Average accuracy: {}".format(self.validation_results['average_accuracy']))

        predictions = self.network.predict(x_test)
        y_test = np.array(y_test, dtype=np.int)
        mean_kappa = 0
        for i in range(0, y_test.shape[1]):
            kappa = cohen_kappa_score(y_test[:, [i]], predictions[:, [i]])
            self.validation_results['kappa_class_{}'.format(i + 1)] = kappa
            log_function("Kappa class {}: {}".format(i + 1, kappa))
            mean_kappa += kappa
        self.validation_results['average_kappa'] = mean_kappa/6
        log_function("Average Kappa: {}".format(self.validation_results['average_kappa']))
        self.validation_results['report'] = classification_report(y_test, predictions)
        log_function("\n" + self.validation_results['report'])

    def train_image(self, band_data, classes_data, max_iter, no_data_value=0, test_size=0.33, log_function=print):
        """
        The given network can be trained given an image of different band waves (band_data) and a respectively data set
        indicating a subset of different classes of the image (class_data).

        :param ndarray band_data: array with all bands
        :param ndarray classes_data: an overlap image indicating different classes
        :param int max_iter: the number of iterations when training the neural network
        :param int no_data_value: value that describes pixels with no data in the classes_data file
        :param float test_size: the proportion of the test_size that will be used to evaluate the trained network
        :param log_function: function to log
        """

        if band_data.ndim < 2:
            raise ValueError("This method requires more than one band.")

        # flatten input
        bands_flattened = band_data.reshape(len(band_data), -1).transpose()
        classes_flattened = classes_data.flatten()
        del band_data
        del classes_data

        # useful indices
        good_indices = np.where(classes_flattened != no_data_value)[0]

        # prepare x and y as trainings input
        x = bands_flattened[good_indices, :]

        classes = classes_flattened[good_indices]
        self.unique_classes = np.unique(classes)

        y = np.zeros((len(good_indices), len(self.unique_classes)))
        for i, this_class in enumerate(self.unique_classes):
            find_class = np.where(classes == this_class)
            y[find_class, i] = 1

        self.network.max_iter = max_iter
        if test_size:
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
            self.network.fit(x_train, y_train)
            self.validate(x_test, y_test, log_function)
        else:
            self.network.fit(x, y)

    def predict_image(self, band_data, probability_of_class=None):
        """
        Use the trained network, it is possible to classify the complete image using the different bands of the image.
        If probability_of_class is given, than the image will show the probability that this class will occur.

        :param ndarray band_data: array with all bands
        :param int probability_of_class: class for which you would like the probability image
        :return: ndarray classified_image: the classified image
        """

        # predict classes or get probability for every row of the image
        bands_flattened = band_data.reshape(len(band_data), -1).transpose()
        prediction = self.network.predict_proba(bands_flattened)
        if probability_of_class is None:
            # set image pixel equal to the class with highest probability
            best_prediction = np.argmax(prediction, axis=1)
            output_flattened = self.unique_classes[best_prediction]
        else:
            # set the image pixel equal to the probability of the given class
            class_location = np.where(self.unique_classes == probability_of_class)[0][0]
            output_flattened = prediction[:, class_location]

        return output_flattened.transpose().reshape(band_data[0].shape)
