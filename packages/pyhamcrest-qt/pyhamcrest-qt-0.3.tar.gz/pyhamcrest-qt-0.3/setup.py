# pyhamcrest-qt - PyHamcrest extensions for use with Qt (either pyside2 or PyQt5)
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
from distutils.core import setup

setup(
    name="pyhamcrest-qt",
    packages=["qtmatchers"],
    version="0.3",
    license="GNU GPL v3+",
    description="PyHamcrest extensions for use with Qt (either pyside2 or PyQt5)",
    author="Kamil Strzempowicz",
    author_email="konserw@gmail.com",
    url="https://github.com/konserw/pyhamcrest-qt",
    download_url="https://github.com/konserw/pyhamcrest-qt/archive/v0.3.zip",
    keywords=["Hamcrest", "pyHamcrest", "Qt", "pyside2", "PyQt5", "matchers"],
    install_requires=[
        "Qt5.py",
        "PyHamcrest",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
)
