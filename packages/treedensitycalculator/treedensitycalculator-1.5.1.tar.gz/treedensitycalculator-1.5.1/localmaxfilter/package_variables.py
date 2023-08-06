# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : April 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
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
from os import path

package_name_pip = 'treedensitycalculator'
qgis_plugin_name = 'Tree Density Calculator'
read_the_docs_name = 'TreeDensityCalculator'
sphinx_title = 'Tree Density Calculator Documentation'

author = 'Ann Crabbé (KU Leuven); Tinne Cahy (Geo Solutions)'
author_doc = 'Ann Crabbé (KU Leuven)'
author_email = 'acrabbe.foss@gmail.com'
author_copyright = '© 2018 - 2020 by Ann Crabbé (KU Leuven)'
short_version = '1.5'
long_version = '1.5.1'

bitbucket_home = 'https://bitbucket.org/kul-reseco/localmaxfilter'
bitbucket_src = 'https://bitbucket.org/kul-reseco/localmaxfilter/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/localmaxfilter/issues'

read_the_docs = 'https://treedensitycalculator.readthedocs.io'

keywords = ['forestry', 'tree density', 'remote sensing']

qgis_min_version = '3.6'

short_description = 'The Tree Density Calculator is a QGIS plugin and command line interface package designed to ' \
                    'calculate tree densities based on brightness images.'
long_description = 'The Tree Density Calculator is a QGIS plugin and command line interface package designed to ' \
                    'calculate tree densities based on brightness images, using the local maximum of a sliding window.'

icon = 'images/lumos_h50.png'
qgis_category = 'Raster'
