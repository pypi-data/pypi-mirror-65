#!/usr/bin/env python

from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'docs', 'README.pypi.rst'), encoding='utf-8') as f:
    long_description = f.read()

# blink2png-bridge  Copyright (C) 2020 Star Inc.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

setup(
    name="blink2png-bridge",
    version='0.1.2',
    url='http://github.com/star-inc/blink2png-bridge',
    license='GNU Lesser General Public License',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    description='To via blink2png by Python directly.',
    author='Star Inc.',
    author_email='"Star Inc." <star_inc@aol.com>',
    packages=['blink2png_bridge'],
    zip_safe=True,
    include_package_data=True,
    package_dir=[],
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
        'Topic :: Utilities'
    ], install_requires=['blink2png']
)
