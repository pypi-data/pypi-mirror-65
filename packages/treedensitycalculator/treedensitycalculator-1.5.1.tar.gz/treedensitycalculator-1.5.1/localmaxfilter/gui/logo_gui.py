# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : September 2018
| Copyright           : © 2018 - 2020 by Ann Crabbé (KU Leuven)
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
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QWidget, QLabel, QHBoxLayout
from qgis.PyQt.QtCore import Qt
from localmaxfilter.resources_rc import qInitResources
qInitResources()


class LogoWidget(QWidget):
    """ QWidget with the project's logo. To be placed above each widget/dialog. """

    def __init__(self, parent=None):
        super(LogoWidget, self).__init__(parent=parent)

        self.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignHCenter)

        lumos = QLabel(self)
        lumos.setContentsMargins(0, 0, 0, 0)
        lumos.setPixmap(QPixmap(':/lumos_full'))
        layout.addWidget(lumos)

        # gent = QLabel(self)
        # gent.setContentsMargins(0, 0, 0, 0)
        # gent.setPixmap(QPixmap(':/logo_gent'))
        # layout.addWidget(gent)


def _run():
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.initQgis()

    z = LogoWidget()
    z.show()
    app.exec_()


if __name__ == '__main__':
    _run()
