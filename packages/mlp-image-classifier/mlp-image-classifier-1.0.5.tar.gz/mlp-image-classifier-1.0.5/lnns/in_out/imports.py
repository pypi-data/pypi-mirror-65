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
import os
import numpy as np
from osgeo import gdal


class PatternFile:
    def __init__(self, number_of_patterns, input_neurons, output_neurons, x, y):
        self.number_of_patterns = number_of_patterns
        self.input_neurons = input_neurons
        self.output_neurons = output_neurons
        self.x = x
        self.y = y


def read_pattern(path_prn):
    x_list = []
    y_list = []
    with open(path_prn) as open_file:
        filedata = open_file.readlines()
    if "number_of_patterns: " not in filedata[0] or \
            "number_of_inputs: " not in filedata[1] or "number_of_outputs: " not in filedata[2]:
        raise ValueError("Invalid prn file: The first lines must contain: "
                         "\nnumber_of_patterns: \nnumber_of_inputs: \nnumber_of_outputs: ")
    number_of_patterns = int(filedata[0].split("number_of_patterns: ")[1])
    input_neurons = int(filedata[1].split("number_of_inputs: ")[1])
    output_neurons = int(filedata[2].split("number_of_outputs: ")[1])
    data = filedata[4:]
    for line in data:
        xy_line = line.split(' ')
        x_list.append(xy_line[:input_neurons])
        if output_neurons > 0:
            y_list.append(xy_line[input_neurons:output_neurons + input_neurons])
    return PatternFile(
        number_of_patterns=number_of_patterns,
        input_neurons=input_neurons,
        output_neurons=output_neurons,
        x=np.array(x_list, dtype=np.double).transpose(),
        y=np.array(y_list, dtype=np.double).transpose() if y_list else None
    )


def import_image(path, reflectance=False):
    """ Browse for an image.

    :param path: the absolute path to the image
    :param reflectance: return reflectance values instead of DN between 0 and 254
    :return: float32 numpy array [#good bands x #rows x #columns]
    """

    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        array = data.ReadAsArray()
        metadata = {'geo_transform': data.GetGeoTransform(), 'x_size': data.RasterXSize, 'y_size': data.RasterYSize,
                    'projection': data.GetProjection()}

        if reflectance and array.max() > 1:
            array = array / float(255)  # adjust to reflectance values

        # in order to be able to concatenate 2D-bands with 3D images
        if array.ndim <= 2:
            array = np.expand_dims(array, 0)

        return array, metadata

    except Exception as e:
        raise Exception(str(e))


def check_path(path):
    """ Check if path exists. Skipp path which are in memory

    :param path: the absolute path to the input file
    """
    if path == '':
        pass

    elif 'vsimem' in path:
        pass

    elif not os.path.exists(path):
        raise Exception("Cannot find file '" + path + "'.")
