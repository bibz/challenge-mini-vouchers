#!/usr/bin/env python
#
# Copyright 2019 Borjan Tchakaloff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""The setup script."""

from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    README = readme_file.read()


setup(
    author="Borjan Tchakaloff",
    author_email="borjan@tchakaloff.fr",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
    ],
    description="A minimal implementation of a voucher system.",
    license="GNU General Public License v3 or later",
    long_description=README,
    name="mini-vouchers",
    packages=find_packages(include=["mini_vouchers"]),
    python_requires="~=3.6",
    version="0.1.0",
)
