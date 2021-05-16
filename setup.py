#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL


import versiontools_support
from setuptools import setup, find_packages

setup(
    name = 'taiga_miem_middleware',
    version = ":versiontools:taiga_miem_middleware:",
    description = "The Taiga plugin for middleware between MIEM Services",
    long_description = "",
    keywords = 'taiga, miem, middleware',
    author = 'Vladislav Kovyazin',
    author_email = 'vvkovyazin@miem.hse.ru',
    url = '',
    license = 'MPL-2',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 1 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)