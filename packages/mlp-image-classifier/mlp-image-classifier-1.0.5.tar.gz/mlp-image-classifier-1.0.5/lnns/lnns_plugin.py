# -*- coding: utf-8 -*-
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
from os import path
from functools import partial

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget, QMenu
from qgis.core import QgsApplication

from lnns.gui.lnns_gui import NeuralNetworkWidget
from lnns.lnns_provider import NeuralNetworkProvider
from lnns.resources_rc import qInitResources
qInitResources()


class NeuralNetworkPlugin:
    """ QGIS Plugin Implementation """

    def __init__(self, iface):
        """
        :param QgsInterface iface: the interface instance which provides the hook to manipulate the QGIS GUI at run time
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)

        # List of actions added by this plugin
        self.actions = []

        # Add an empty menu to the Raster Menu
        self.main_menu = QMenu(title='Neural Network MLPClassifier', parent=self.iface.rasterMenu())
        self.main_menu.setIcon(QIcon(':/lumos'))
        self.iface.rasterMenu().addMenu(self.main_menu)
        self.provider = None

    def add_action(self, icon_path: str, text: str, callback: callable, enabled_flag: bool = True,
                   status_tip: str = None, whats_this: str = None, parent: QWidget = None)->QAction:
        """ Add a toolbar item to the toolbar.

        :param icon_path: can be a resource path (e.g. ':/plugins/foo/bar.png') or a normal file system path
        :param text: text to be displayed on the menu item
        :param callback: function to be called when the action is triggered
        :param enabled_flag: flag indicating if the action should be enabled by default
        :param status_tip: optional text to show in a popup when mouse pointer hovers over the action
        :param whats_this: optional text to show in the status bar when the mouse pointer hovers over the action
        :param parent: parent widget for the new action
        :returns: The action that was created. Note that the action is also added to self.actions list
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        self.main_menu.addAction(action)
        self.actions.append(action)

        return action

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        self.add_action(icon_path=':/lumos',
                        text='Neural Network MLPClassifier',
                        callback=partial(self.run, 'lnns'),
                        status_tip='Predict image classes using supervised classification (MLPClassifier).',
                        parent=self.iface.mainWindow())

        self.initProcessing()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.rasterMenu().removeAction(self.main_menu.menuAction())
        QgsApplication.processingRegistry().removeProvider(self.provider)

    @staticmethod
    def run(name: str):
        """Run method that performs all the real work"""
        if name == 'lnns':
            widget = NeuralNetworkWidget()
        else:
            return
        widget.show()
        widget.exec_()

    def initProcessing(self):
        self.provider = NeuralNetworkProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)
