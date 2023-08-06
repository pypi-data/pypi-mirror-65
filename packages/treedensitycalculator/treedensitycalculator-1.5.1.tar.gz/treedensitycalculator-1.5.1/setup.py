# -*- coding: UTF-8 -*-.
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
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
from setuptools import setup, find_packages
from localmaxfilter.package_variables import *
# read the contents of your README file
with open(path.join(path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    read_me = f.read()

setup(
    name=package_name_pip,
    version=long_version,

    description=long_description,
    description_content_type='text/x-rst',
    long_description=read_me,
    long_description_content_type='text/x-rst',
    keywords=keywords,

    author=author,
    author_email=author_email,

    url=bitbucket_home,
    project_urls={
        'Documentation': read_the_docs,
        'Source Code': bitbucket_src,
        'Issue Tracker': bitbucket_issues,
    },

    packages=find_packages(exclude=['*test*']),
    data_files=[("", ["COPYING.txt"])],
    include_package_data=True,
    zip_save=False,

    entry_points={
        'console_scripts':
            [
                'treedensity = localmaxfilter.cli.local_max_filter_cli:main'
            ],
    },

    classifier='License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
)
