# -*- coding: utf-8 -*-

# Copyright (C) 2011  Björn Larsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

setup(
    name = "fuzzycomp",
    version = "0.2.1",
    packages = ["fuzzycomp"],
    author = "Björn Larsson",
    author_email = "fuzzycomp@googlegroups.com",
    url = "http://code.google.com/p/fuzzycomp/",
    download_url = "http://code.google.com/p/fuzzycomp/downloads/list",
    license = "GPLv3",
    description='A package implementing various sequence/string comparison \
                algorithms.',
    keywords = ["comparison", "fuzzy"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Text Processing",
        "Topic :: Utilities"]
)