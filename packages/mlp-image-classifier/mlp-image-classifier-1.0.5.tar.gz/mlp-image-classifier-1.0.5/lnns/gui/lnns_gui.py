# -*- coding: utf-8 -*-
""""""  # for sphinx auto doc purposes
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : December 2019
| Copyright           : © 2019 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
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
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QDialogButtonBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsProviderRegistry, QgsMapLayerProxyModel, QgsRasterLayer, QgsProject
from qgis.utils import iface
from qgis.PyQt.uic import loadUi

from lnns.gui.logo_gui import LogoWidget
from lnns.in_out import EmittingStream, run_algorithm_images, tuple_int


class NeuralNetworkWidget(QDialog):
    """ QDialog to interactively set up the Neural Network input and output. """

    def __init__(self):
        super(NeuralNetworkWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'lnns.ui'), self)

        # Logo
        self.logoLayout.addWidget(LogoWidget(parent=self.logoWidget))

        # input
        open_layers = QgsProject.instance().mapLayers().values()
        self.listWidget.addItems([layer.name() for layer in open_layers if isinstance(layer, QgsRasterLayer)])
        self.listWidget.itemSelectionChanged.connect(self._image_counter)
        self.imageAction.triggered.connect(self._image_browse)
        self.imageButton.setDefaultAction(self.imageAction)
        self.selectAllAction.triggered.connect(self._select_all)
        self.selectAllButton.setDefaultAction(self.selectAllAction)
        self.clearSelectionAction.triggered.connect(self._clear_selection)
        self.clearSelectionButton.setDefaultAction(self.clearSelectionAction)

        # classified image
        excluded_providers = [p for p in QgsProviderRegistry.instance().providerList() if p not in ['gdal']]
        self.classifiedComboBox.setExcludedProviders(excluded_providers)
        self.classifiedComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.classifiedComboBox.layerChanged.connect(self._set_classification_values)
        self._set_classification_values()
        self.classifiedAction.triggered.connect(self._image_classified_browse)
        self.classifiedButton.setDefaultAction(self.classifiedAction)

        # NN parameters
        self.activationFunction.insertItems(0, ['identity', 'logistic', 'tanh', 'relu'])
        self.activationFunction.setCurrentText('logistic')
        self.probabilityValue.setEnabled(False)
        self.probabilityCheckBox.toggled.connect(self._toggle_probability)

        # output
        self.outputFileWidget.lineEdit().setReadOnly(True)
        self.outputFileWidget.lineEdit().setPlaceholderText('[Create temporary layer]')
        self.outputFileWidget.setStorageMode(QgsFileWidget.SaveFile)
        self.outputFileWidget.setFilter("Tiff (*.tif);;All (*.*)")

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openCheckBox.setChecked(False)
            self.openCheckBox.setDisabled(True)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_lnns)
        self.OKClose.rejected.connect(self.close)

        # widget variables
        self.image = None
        self.classified = None

        # log
        self.log = EmittingStream(self.tabWidget).write

    def _image_browse(self, classified=False):
        """ Browse for an image raster file. """
        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileRasterFilters())[0]
        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsRasterLayer(path, os.path.basename(path), 'gdal')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)

                if classified:
                    self.classifiedComboBox.setLayer(layer)
                else:
                    self.listWidget.addItem(layer.name())
                    self.listWidget.item(self.listWidget.count() - 1).setSelected(True)
        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _image_classified_browse(self):
        self._image_browse(True)

    def _image_counter(self):
        self.nb_input.setText("{} layers selected".format(len(self.listWidget.selectedItems())))

    def _select_all(self):
        [self.listWidget.item(i).setSelected(True) for i in range(self.listWidget.count())]

    def _clear_selection(self):
        [self.listWidget.item(i).setSelected(False) for i in range(self.listWidget.count())]

    def _set_classification_values(self):
        """ set the possible values for missing and probability values once a layer is chosen"""
        layer = self.classifiedComboBox.currentLayer()
        if layer is None:
            return
        try:
            block = layer.dataProvider().block(1, layer.extent(), layer.width(), layer.height())
            row = np.repeat(np.arange(0, layer.height()), layer.width())
            col = np.tile(np.arange(0, layer.width()), layer.height())
            data = [block.value(x, y) for x, y in zip(row, col)]

            # a short list of unique values
            unique_classes = np.unique(np.array(data))
            unique_classes = ['{:.0f}'.format(x) for x in unique_classes]
            unique_classes = [''] + unique_classes

            # add them to the drop down menus
            self.noDataValue.clear()
            self.noDataValue.insertItems(0, unique_classes)
            self.probabilityValue.clear()
            self.probabilityValue.insertItems(0, unique_classes)

            # in case the tiff image has a no data value set, use this one automatically
            no_data_value = '{:.0f}'.format(block.noDataValue())
            if no_data_value in unique_classes:
                self.noDataValue.setCurrentIndex(unique_classes.index(no_data_value))
        except Exception as e:
            self.log(e)

    def _update_process_bar(self, value):
        self.progressBar.setValue(value)

    def _toggle_probability(self, value):
        self.probabilityValue.setEnabled(value)

    def _run_lnns(self):
        """ Read all parameters and pass them on to the Network class. """
        try:
            # Only temp file possible when result is opened in QGIS
            if not self.openCheckBox.isChecked() and len(self.outputFileWidget.filePath()) == 0:
                raise Exception("If you won't open the result in QGIS, you must select a base file name for output.")

            # Get parameters
            all_layers = QgsProject.instance().mapLayers().values()
            selected_layer_names = [item.text() for item in self.listWidget.selectedItems()]
            image_paths = [layer.source() for layer in all_layers if layer.name() in selected_layer_names]
            hidden_layer_size = tuple_int(self.hiddenNeurons.text())
            iterations = self.maxIterations.value()
            activation = self.activationFunction.currentText()
            classified_path = self.classifiedComboBox.currentLayer().source()
            no_data_value = self.noDataValue.currentText()
            no_data_value = None if no_data_value == '' else int(no_data_value)
            test_size = self.testSize.value()
            if self.probabilityCheckBox.isChecked():
                probability_of_class = self.probabilityValue.currentText()
                if probability_of_class == '':
                    raise Exception("Choose for which class the probability should be calculated.")
                else:
                    probability_of_class = int(probability_of_class)
            else:
                probability_of_class = None
            output_path = self.outputFileWidget.filePath()

            # run LNNS
            result = run_algorithm_images(image_paths=image_paths,
                                          hidden_layer_size=hidden_layer_size,
                                          iterations=iterations,
                                          activation=activation,
                                          classified_path=classified_path,
                                          no_data_value=no_data_value,
                                          test_size=test_size,
                                          probability_of_class=probability_of_class,
                                          update_process_bar=self._update_process_bar,
                                          log_function=self.log,
                                          output_path=output_path)

            # Open result in QGIS
            if self.openCheckBox.isChecked():
                output_raster_layer = QgsRasterLayer(result, os.path.splitext(os.path.basename(result))[0])
                QgsProject.instance().addMapLayer(output_raster_layer, True)

        except AttributeError:
            self.log("Please select a raster with classified pixels for training.")
        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = NeuralNetworkWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
