#!/usr/bin/env python
# https://docs.openstack.org/pbr/latest/user/using.html
"""setup.py"""

import os
from setuptools import setup, find_packages

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    include_package_data=True
)
