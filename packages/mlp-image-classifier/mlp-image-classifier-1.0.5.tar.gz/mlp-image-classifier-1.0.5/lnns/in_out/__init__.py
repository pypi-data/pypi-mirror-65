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
import os
import numpy as np
import pyqtgraph as pg
import tempfile
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  # no error, it works

from osgeo import gdal
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QWidget
app = QgsApplication([], True)

from lnns.in_out.imports import import_image, read_pattern
from lnns.in_out.exports import write_classified_image, write_pattern
from lnns.scripts.network import Network


def tuple_int(s):
    try:
        return tuple(map(int, s.strip().rstrip(',').split(',')))
    except ValueError:
        raise ValueError("The given hidden layer size is incorrect. Example for three layers: 4,5,3.")


def plot(x, y, size=None, title="Neural Network MLPClassifier: Network error decline", testing=False):
    if size is None:
        pg.plot(x, y, labels={'left': 'cost', 'bottom': 'iterations'}, title=title)
    else:
        scatter = pg.ScatterPlotItem(x, y, size=size, title=title)
        pg.plot().addItem(scatter)
    if testing:
        QTimer.singleShot(3000, app.closeAllWindows)
    app.exec_()


def plot_to_file(x, y, path, title="Neural Network MLPClassifier: Network error decline"):
    plt.plot(x, y)
    plt.ylabel('cost')
    plt.xlabel('iterations')
    plt.title(title)
    plt.savefig(path)


def run_algorithm_images(image_paths, classified_path, no_data_value, hidden_layer_size, activation, iterations,
                         test_size, probability_of_class, update_process_bar, log_function,
                         output_path=None, plot_path=None, feedback=None, context=None):
    """
    Process all input, in order to run the nn script.

    :param image_paths: the absolute path to the input raster files
    :param classified_path: absolute path to the classified raster file
    :param no_data_value: value that describes pixels with no data in the classes_data file
    :param hidden_layer_size: Hidden layer size with length = n_layers - 2, comma separated values.
    :param activation: Activation function for the MLPClassifier, choices=['identity', 'logistic', 'tanh', 'relu']
    :param iterations: Maximum number of iterations
    :param test_size: the proportion of the test_size that will be used to evaluate the trained network
    :param probability_of_class: class for which you would like the probability image
    :param update_process_bar: function to update the progress bar
    :param log_function: function to log
    :param output_path: path for output files (optional)
    :param plot_path: necessary for the processing tool: path for the plot
    :param feedback: necessary for the processing tool
    :param context: necessary for the processing tool
    :return: output path
    """
    # check input is not empty
    if not image_paths:
        raise Exception("Please select image file(s).")

    try:
        # get images and metadata
        images, metadata = map(list, zip(*[import_image(path, True) for path in image_paths]))
        classes_data, class_img_metadata = import_image(classified_path)
        metadata.append(class_img_metadata)

        # check all images have the same metadata:
        s1, s2, = zip(*[(m['x_size'], m['y_size']) for m in metadata])
        g1, g2, g3, g4, g5, g6 = zip(*[(m['geo_transform']) for m in metadata])

        if (s1[1:] != s1[:-1]) or (s2[1:] != s2[:-1]):
            raise Exception("All images must have the same number of rows and columns.")
        if (g1[1:] != g1[:-1]) or (g2[1:] != g2[:-1]) or (g3[1:] != g3[:-1]) or (g4[1:] != g4[:-1]) or \
                (g5[1:] != g5[:-1]) or (g6[1:] != g6[:-1]):
            raise Exception("All images must have the same geographical parameters.")

        # merge bands into one array
        band_data = np.concatenate(images)

        # create network
        net = Network(number_of_hidden=hidden_layer_size, activation=activation)
        update_process_bar(25)

        # train the network
        net.train_image(band_data=band_data, classes_data=classes_data, max_iter=iterations,
                        no_data_value=no_data_value, test_size=test_size, log_function=log_function)
        if feedback or plot_path:
            plot_to_file(x=range(len(net.network.loss_curve_)), y=net.network.loss_curve_, path=plot_path)
        else:
            plot(range(len(net.network.loss_curve_)), net.network.loss_curve_)
        update_process_bar(50)

        # predict the network
        classified_image = net.predict_image(band_data=band_data, probability_of_class=probability_of_class)
        update_process_bar(100)

        # output
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), os.path.splitext(os.path.basename(image_paths[0]))[0])
            output_path = '{0}_predict.tif'.format(output_path)

        # classified image
        gdal_type = gdal.GDT_Int16 if probability_of_class is None else gdal.GDT_Float64
        output_path = write_classified_image(output_path, classified_image, class_img_metadata['geo_transform'],
                                             class_img_metadata['projection'], gdal_type)
        return output_path
    except Exception as e:
        log_function(e)


def run_algorithm_pattern(pattern_train, pattern_predict, no_data_value, hidden_layer_size, activation, iterations,
                          test_size, probability_of_class, log_function,
                          output_path=None, plot_path=None, feedback=None, context=None):
    """
    Process all input, in order to run the nn script.

    :param pattern_train: the absolute path to the pattern file with training data
    :param pattern_predict: absolute path to the pattern file for predictions
    :param no_data_value: value that describes pixels with no data in the classes_data file
    :param hidden_layer_size: Hidden layer size with length = n_layers - 2, comma separated values.
    :param activation: Activation function for the MLPClassifier, choices=['identity', 'logistic', 'tanh', 'relu']
    :param iterations: Maximum number of iterations
    :param test_size: the proportion of the test_size that will be used to evaluate the trained network
    :param probability_of_class: class for which you would like the probability image
    :param log_function: function to log
    :param output_path: path for output files (optional)
    :param plot_path: necessary for the processing tool: path for the plot
    :param feedback: necessary for the processing tool
    :param context: necessary for the processing tool
    :return: output path
    """
    try:
        train_prn = read_pattern(pattern_train)
        predict_prn = read_pattern(pattern_predict)
        if train_prn.input_neurons != predict_prn.input_neurons:
            raise Exception("The input file and file to predict must contain the same number of input_neurons.")

        # create network
        net = Network(number_of_hidden=hidden_layer_size, activation=activation)

        # train the network
        net.train_image(band_data=train_prn.x, classes_data=train_prn.y, max_iter=iterations,
                        no_data_value=no_data_value, test_size=test_size, log_function=log_function)

        if feedback or plot_path:
            plot_to_file(x=range(len(net.network.loss_curve_)), y=net.network.loss_curve_, path=plot_path)
        else:
            plot(x=range(len(net.network.loss_curve_)), y=net.network.loss_curve_)

        # predict the network
        y_predict = net.predict_image(band_data=predict_prn.x, probability_of_class=probability_of_class)

        # output
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), os.path.splitext(os.path.basename(pattern_predict))[0])
            output_path = '{0}_predict.tif'.format(output_path)

        # classified image
        x_y_predict = np.around(np.concatenate((predict_prn.x.transpose(), y_predict[:, None]), axis=1), decimals=2)
        write_pattern(output_path, predict_prn.number_of_patterns, train_prn.input_neurons, train_prn.output_neurons,
                      x_y_predict, '%.2f')

        return output_path
    except Exception as e:
        log_function(e)


class EmittingStream:
    """ QObject to catch the terminal output and send it along with pyqtSignal. """

    def __init__(self, tab_widget):

        self.tab_widget = tab_widget
        self.log_index = tab_widget.indexOf(tab_widget.findChild(QWidget, 'tab_log'))
        self.log_widget = tab_widget.findChild(QWidget, 'logBrowser')

    def write(self, text):
        text = str(text)
        self.log_widget.append(text)
        self.tab_widget.setCurrentIndex(self.log_index)
