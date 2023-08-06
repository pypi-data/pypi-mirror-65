# -*- coding: utf-8 -*-
""""""  # for sphinx auto doc purposes
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : September 2018
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
from os.path import abspath, join
import argparse

from lnns.cli import tuple_int, tuple_string
from lnns.in_out import run_algorithm_images
from lnns.scripts.network import Network


def create_parser():
    parser = argparse.ArgumentParser(description=str(Network.__doc__))

    parser.add_argument('images_folder', type=str,
                        help='Path to the input image data and the classes data.')
    parser.add_argument('image_names', type=tuple_string,
                        help='Name(s) of different image bands.')
    parser.add_argument('classes_data_name', type=str,
                        help='Name of an overlap image indicating different classes')
    parser.add_argument('-n', '--no_data_value', type=int, default=-1,
                        help='Value that describes pixels with no data in the classes_data file (default: -1).')

    # optional
    parser.add_argument('-l', '--hidden_layer_size', type=tuple_int, default=(10,),
                        help='Hidden layer size with length = n_layers - 2, comma separated values. The ith element '
                             'represents the number of neurons in the ith hidden layer. (default: 10,)')
    parser.add_argument('-a', '--activation', type=str, choices=['identity', 'logistic', 'tanh', 'relu'],
                        help='Activation function for the MLPClassifier (default: logistic).', default='logistic')
    parser.add_argument('-i', '--iterations', type=int,
                        help='Maximum number of iterations (default: 200).', default=200)
    parser.add_argument('-t', '--test_size', type=float, default=0.33,
                        help='Portion of test pixels used to evaluate the trained network (default: 0.33).')
    parser.add_argument('-p', '--probability_of_class', type=int,
                        help='Class for which you would like the probability image (default: None).', default=None)
    parser.add_argument('-o', '--output',
                        help="Output predicted file (default: in same folder with name 'output_classified.tif'")
    parser.add_argument('-g', '--output_graph',
                        help="Output error graph (default: in same folder with name 'output_error.PNG'")
    return parser


def run_network(args):
    """
    Documentation: mlpclassifier-image -h
    """
    folder_abspath = abspath(args.images_folder)
    image_paths = [join(folder_abspath, image_name) for image_name in args.image_names]
    classified_path = join(folder_abspath, args.classes_data_name)
    output_file = abspath(args.output) if args.output else join(folder_abspath, "output_classified.tif")
    graph_file = abspath(args.output_graph) if args.output_graph else join(folder_abspath, "output_error.PNG")

    def log_function(text):
        print(str(text))

    run_algorithm_images(image_paths=image_paths,
                         classified_path=classified_path,
                         no_data_value=args.no_data_value,
                         hidden_layer_size=args.hidden_layer_size,
                         activation=args.activation,
                         iterations=args.iterations,
                         test_size=args.test_size,
                         probability_of_class=args.probability_of_class,
                         update_process_bar=log_function,
                         log_function=log_function,
                         output_path=output_file,
                         plot_path=graph_file)

    print("Predicted output: {}".format(output_file))
    print("Network error decline: {}".format(graph_file))


def main():
    parser = create_parser()
    run_network(parser.parse_args())


if __name__ == '__main__':
    main()
