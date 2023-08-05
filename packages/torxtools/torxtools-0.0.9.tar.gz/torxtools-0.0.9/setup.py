#!/usr/bin/env python3

import sys
from setuptools import setup, config

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(install_requires=requirements)
