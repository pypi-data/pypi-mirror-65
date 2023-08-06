# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):
    """ Load NeuralNetworkPlugin class.
    :param QgsInterface iface: A QGIS interface instance.
    """
    from lnns.lnns_plugin import NeuralNetworkPlugin
    return NeuralNetworkPlugin(iface)
