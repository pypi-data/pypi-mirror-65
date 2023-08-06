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


def write_pattern(output_file, number_of_patterns, input_neurons, output_neurons, array, fmt):
    header = "\nnumber_of_patterns: {0}\nnumber_of_inputs: {1}\nnumber_of_outputs: {2}\n".format(
        number_of_patterns,
        input_neurons,
        output_neurons
    )
    np.savetxt(output_file, array, fmt=fmt, header=header, comments='')
    with open(output_file) as f:
        lines = f.readlines()
    with open(output_file, 'w') as f:
        f.writelines(lines[1:])


def write_classified_image(file_path, image, geo_transform=None, projection=None, gdal_type=gdal.GDT_Int16):

    gdal.UseExceptions()
    driver = gdal.GetDriverByName('GTiff')
    try:
        raster = driver.Create(file_path, image.shape[1], image.shape[0], 1, gdal_type)
    except RuntimeError:
        # file is still open in QGIS so cannot be overwritten --> create new filename that does not exist
        while os.path.exists(file_path):
            base, ext = os.path.splitext(file_path)
            file_path = '{0}_1{1}'.format(base, ext)
        raster = driver.Create(file_path, image.shape[1], image.shape[0], 1, gdal_type)

    raster.GetRasterBand(1).WriteArray(image)
    raster.GetRasterBand(1).SetDescription('classification')

    if geo_transform:
        raster.SetGeoTransform(geo_transform)
    if projection:
        raster.SetProjection(projection)
    raster.FlushCache()

    return file_path
