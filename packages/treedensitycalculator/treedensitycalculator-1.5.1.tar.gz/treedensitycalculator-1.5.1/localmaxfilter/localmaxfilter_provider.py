# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : November 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
|
| This file is part of the QGIS Tree Density Calculator plugin and treedensitycalculator python package.
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
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from localmaxfilter.localmaxfilter_processing import LocalMaxFilterProcessingAlgorithm


class LocalMaxFilterProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(LocalMaxFilterProcessingAlgorithm())

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider. This string should be a unique, short,
        character only string, eg "qgis" or "gdal". This string should not be localised. """
        return 'lumos:tree_density'

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing. This string should be as short as possible
        (e.g. "Lastools", not "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('Tree Density')

    def icon(self):
        """ Should return a QIcon which is used for your provider inside the Processing toolbox. """
        return QIcon(':/lumos')
