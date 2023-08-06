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
import argparse
from os import path as op

from lnns.cli import tuple_int
from lnns.in_out import run_algorithm_pattern
from lnns.scripts.network import Network


def create_parser():
    parser = argparse.ArgumentParser(description=str(Network.__doc__))

    # library
    parser.add_argument('pattern_train_path', type=str,
                        help="Pattern text file that includes the network training values, 'number_of_patterns', "
                             "'number_of_inputs' and 'number_of_outputs.'")
    parser.add_argument('pattern_predict_path', type=str,
                        help="Pattern text file that includes the values to predict,'number_of_patterns', "
                             "'number_of_inputs' and 'number_of_outputs.'")
    parser.add_argument('-l', '--hidden_layer_size', type=tuple_int, default=(10,),
                        help='Hidden layer size with length = n_layers - 2, comma separated values. The ith element '
                             'represents the number of neurons in the ith hidden layer. (default: 10,)')
    parser.add_argument('-a', '--activation', type=str, choices=['identity', 'logistic', 'tanh', 'relu'],
                        help='Activation function for the MLPClassifier (default: logistic).', default='logistic')
    parser.add_argument('-i', '--iterations', type=int,
                        help='Maximum number of iterations (default: 200).', default=200)
    parser.add_argument('-n', '--no_data_value', type=int, default=-1,
                        help='Value that describes pixels with no data in the classes_data file (default: -1).')
    parser.add_argument('-t', '--test_size', type=float, default=0.33,
                        help='Portion of test pixels used to evaluate the trained network (default: 0.33).')
    parser.add_argument('-p', '--probability_of_class', type=int,
                        help='class for which you would like the probability image (default: None).', default=None)
    parser.add_argument('-o', '--output',
                        help="Output predicted file (default: in same folder with extension '_predict.prn'")
    return parser


def run_network(args):
    """
    Documentation: mlpclassifier-pattern -h
    """
    output_file = args.output if args.output else op.join(op.splitext(args.path_prn_predict)[0], "_predict.prn")

    def log_function(text):
        print(str(text))

    run_algorithm_pattern(pattern_train=args.pattern_train_path,
                          pattern_predict=args.pattern_predict_path,
                          no_data_value=args.no_data_value,
                          hidden_layer_size=args.hidden_layer_size,
                          activation=args.activation,
                          iterations=args.iterations,
                          test_size=args.test_size,
                          probability_of_class=args.probability_of_class,
                          log_function=log_function,
                          output_path=output_file)


def main():
    parser = create_parser()
    run_network(parser.parse_args(), parser)


if __name__ == '__main__':
    main()
