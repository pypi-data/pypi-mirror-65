#!/usr/bin/env python3
#
# Copyright (C) 2019-2020 Cochise Ruhulessin
#
# This file is part of python-iam.
#
# python-iam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# python-iam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-iam.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import find_packages
from setuptools import setup

requirements = str.split(open('requirements.txt').read(), '\n')

setup(
    name='python-iam',
    version='0.2.18',
    description='Identity and Access Management for Python',
    author='Cochise Ruhulessin',
    author_email='cochise.ruhulessin@digitalcitizen.nl',
    url='https://gitlab.com/unimatrixone/libraries/python-iam',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing"
    ]
)
