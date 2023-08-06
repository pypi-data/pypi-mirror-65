# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : April 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
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
package_name_pip = 'mlp-image-classifier'
qgis_plugin_name = 'Neural Network MLPClassifier'
read_the_docs_name = 'NeuralNetworkMLPClassifier'
sphinx_title = 'Neural Network MLPClassifier Documentation'

author = 'Tinne Cahy (Geo Solutions); Ann Crabbé (KU Leuven)'
author_doc = 'Ann Crabbé (KU Leuven)'
author_email = 'acrabbe.foss@gmail.com'
author_copyright = '© 2018 - 2020 by Ann Crabbé (KU Leuven)'
short_version = '1.0'
long_version = '1.0.3'

bitbucket_home = 'https://bitbucket.org/kul-reseco/lnns'
bitbucket_src = 'https://bitbucket.org/kul-reseco/lnns/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/lnns/issues'

read_the_docs = 'https://mlp-image-classifier.readthedocs.io'

keywords = ['supervised classification', 'neural network', 'remote sensing', 'mlp', 'multi-layer perception classifier',
            'image classification']

qgis_min_version = '3.12'

short_description = 'The Neural Network MLPClassifier predicts classified images using supervised classification.'
long_description = 'Supervised classification of an multi-band image using an MLP (Multi-Layer Perception) Neural ' \
                   'Network Classifier. Based on the Neural Network MLPClassifier by scikit-learn:' \
                   'https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html'

icon = 'images/lumos_h50.png'
qgis_category = 'Raster'

processing_provider = 'yes'
