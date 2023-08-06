# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from Local Maximum Filter [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
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
import os
import tempfile

import osgeo.gdal as gdal
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QDialogButtonBox, QWidget
from qgis.gui import QgsFileWidget
from qgis.core import QgsProviderRegistry, QgsMapLayerProxyModel, QgsRasterLayer, QgsProject, QgsVectorLayer
from qgis.utils import iface
from qgis.PyQt.uic import loadUi

from localmaxfilter.scripts.local_max_filter import LocalMaxFilter
from localmaxfilter.gui.logo_gui import LogoWidget
from localmaxfilter.in_out.imports import import_image, import_vector_as_image
from localmaxfilter.in_out.exports import write_mask_layer, write_point_layer, write_voronoi_layer


class LocalMaxFilterWidget(QDialog):
    """ QDialog to interactively set up the Local Max Filter input and output. """

    def __init__(self):
        super(LocalMaxFilterWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'local_max_filter.ui'), self)

        # Logo
        self.logoLayout.addWidget(LogoWidget(parent=self.logoWidget))

        # parameters
        excluded_providers = [p for p in QgsProviderRegistry.instance().providerList() if p not in ['gdal']]
        self.imageComboBox.setExcludedProviders(excluded_providers)
        self.imageComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.imageAction.triggered.connect(self._image_browse)
        self.imageButton.setDefaultAction(self.imageAction)

        excluded_providers = [p for p in QgsProviderRegistry.instance().providerList() if p not in ['ogr']]
        self.maskComboBox.setExcludedProviders(excluded_providers)
        self.maskComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.maskAction.triggered.connect(self._vector_browse)
        self.maskButton.setDefaultAction(self.maskAction)

        # set snap_distance maximum to half of the window size
        self.SNAPSpinBox.setMaximum(self.windowSpinBox.value()/2)
        self.windowSpinBox.valueChanged.connect(self._spinbox_value_changed)

        self.outputFileWidget.lineEdit().setReadOnly(True)
        self.outputFileWidget.lineEdit().setPlaceholderText('[Create temporary layer]')
        self.outputFileWidget.setStorageMode(QgsFileWidget.SaveFile)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openCheckBox.setChecked(False)
            self.openCheckBox.setDisabled(True)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_local_max_filter)
        self.OKClose.rejected.connect(self.close)

        # widget variables
        self.image = None
        self.mask = None

        # log
        self.log = EmittingStream(self.tabWidget).write

    def _image_browse(self):
        """ Browse for an image raster file. """
        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileRasterFilters())[0]
        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsRasterLayer(path, os.path.basename(path), 'gdal')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)
                self.imageComboBox.setLayer(layer)
        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _vector_browse(self):
        """ Browse for a vector file. """
        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileVectorFilters())[0]
        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsVectorLayer(path, os.path.basename(path), 'ogr')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)
                self.maskComboBox.setLayer(layer)
        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _update_process_bar(self, value):
        try:
            self.progressBar.setValue(value)
        except Exception as e:
            self.log(e)

    def _spinbox_value_changed(self, value):
        self.SNAPSpinBox.setMaximum(value/2)

    @staticmethod
    def run_algorithm_local_max_filter(image_path, window, update_process_bar, log_function,
                                       mask_path=None, output_base_path=None,  snap_distance=None, voronoi=None,
                                       feedback=None, context=None):
        """
        Get ready to run the LMF tool

        :param image_path: the absolute path to the raster file
        :param window: window size in meters
        :param update_process_bar: function to update the progress bar
        :param log_function: function to log
        :param mask_path: absolute path to the vector file (optional)
        :param output_base_path: base path for output files (optional)
        :param snap_distance: snap distance for output points (optional)
        :param voronoi: set to True if you want voronoi polygons as output (optional)
        :param feedback: necessary for the processing tool
        :param context: necessary for the processing tool
        :return:
        """

        # check if the image is not none
        if image_path is None:
            raise Exception("Choose a correct image file.")

        # get raster (clipped by mask) and its metadata
        img, img_srs, img_gt = import_image(image_path, mask_path, window)

        # get area of interest as raster
        area_raster = import_vector_as_image(mask_path, img_gt, img.shape, img_srs, window) if mask_path else None

        # convert the window size from meters to number of pixels (odd number)
        pixel_size = img_gt[1]
        window_px = int((window / pixel_size) // 2 * 2 + 1)
        if window_px == 1:
            window_px = 3

        # Print in the log the size of the window in pixels
        log_function('The window is built out of {0} by {0} pixels'.format(window_px))

        if snap_distance:
            if snap_distance > window / 2:
                raise Exception('Snap distance should be max half of the window size')
            snap_distance = int(snap_distance / pixel_size)
            # Print in the log the snap distance in pixels
            log_function('The snap distance is {0} pixels'.format(snap_distance))

        # Run LMF
        lmf_result = LocalMaxFilter(window_px).execute(img, area_of_interest=area_raster, snap=snap_distance,
                                                       geo_transform=img_gt, p=update_process_bar)
        update_process_bar(100)

        # base name for output files
        if not output_base_path:
            output_base_path = os.path.join(tempfile.gettempdir(),  os.path.basename(os.path.splitext(image_path)[0]))
        else:
            output_base_path, _ = os.path.splitext(output_base_path)
        output_base_path = '{0}_window_{1}'.format(output_base_path, window_px)

        # point layer
        output_point_path = output_base_path + '_point.shp'
        write_point_layer(output_point_path, lmf_result, img_gt, img_srs, mask_path)

        # Output mask in case it was given:
        if mask_path:
            output_mask_path = output_base_path + '_mask.shp'
            write_mask_layer(output_mask_path, mask_path, output_point_path)
        else:
            output_mask_path = None

        # write point layer to Voronoi polygon layer
        if voronoi:
            output_voronoi_path = output_base_path + '_voronoi.shp'
            write_voronoi_layer(output_voronoi_path, output_point_path, mask_path)
        else:
            output_voronoi_path = None

        return output_point_path, output_mask_path, output_voronoi_path

    def _run_local_max_filter(self):
        """ Read all parameters and pass them on to the LocalMaxFilter class. """

        try:
            # Only temp file possible when result is opened in QGIS
            if not self.openCheckBox.isChecked() and len(self.outputFileWidget.filePath()) == 0:
                raise Exception("If you won't open the result in QGIS, you must select a base file name for output.")

            # Get parameters
            if not self.imageComboBox.currentLayer():
                raise Exception("Choose a correct image file.")
            else:
                image_path = self.imageComboBox.currentLayer().source()
            window = self.windowSpinBox.value()
            if self.maskComboBox.currentLayer():
                mask_path = self.maskComboBox.currentLayer().source()
            else:
                mask_path = None
            snap_distance = self.SNAPSpinBox.value()
            output_path = self.outputFileWidget.filePath()
            voronoi = self.VoronoiCheckBox.isChecked()

            result = self.run_algorithm_local_max_filter(image_path, window, self._update_process_bar,
                                                         self.log, mask_path, output_path, snap_distance, voronoi)

            # Open result in QGIS
            if self.openCheckBox.isChecked():
                # point layer
                output_point_path = result[0]
                output_point_name, _ = os.path.splitext(os.path.basename(output_point_path))
                output_point_layer = QgsVectorLayer(output_point_path, name=output_point_name)
                QgsProject.instance().addMapLayer(output_point_layer, True)

                # mask layer
                if mask_path:
                    output_mask_path = result[1]
                    output_mask_name, _ = os.path.splitext(os.path.basename(output_mask_path))
                    output_mask_layer = QgsVectorLayer(output_mask_path, name=output_mask_name)
                    QgsProject.instance().addMapLayer(output_mask_layer, True)

                # voronoi layer
                if voronoi:
                    output_voronoi_path = result[2]
                    output_voronoi_name, _ = os.path.splitext(os.path.basename(output_voronoi_path))
                    output_voronoi_layer = QgsVectorLayer(output_voronoi_path, name=output_voronoi_name)
                    QgsProject.instance().addMapLayer(output_voronoi_layer, True)

        except Exception as e:
            self.log(e)


class EmittingStream:
    """ QObject to catch the terminal output and send it along with q pyqtSignal. """

    def __init__(self, tab_widget):

        self.tab_widget = tab_widget
        self.log_index = tab_widget.indexOf(tab_widget.findChild(QWidget, 'tab_log'))
        self.log_widget = tab_widget.findChild(QWidget, 'logBrowser')

    def write(self, text):
        text = str(text)
        self.log_widget.append(text)
        self.tab_widget.setCurrentIndex(self.log_index)

    def flush(self):
        pass


def _run():
    from qgis.core import QgsApplication
    from qgis.analysis import QgsNativeAlgorithms
    app = QgsApplication([], True)
    app.initQgis()
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    z = LocalMaxFilterWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
