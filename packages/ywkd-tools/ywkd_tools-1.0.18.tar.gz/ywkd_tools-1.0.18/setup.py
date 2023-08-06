# -*- coding: utf-8 -*-

import os
import sys
import setuptools
from setuptools import setup


path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))


with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='ywkd_tools',
    version='1.0.18',
    description='娱网科道内部python 公用包',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ywkd',
    author_email='',
    url='',
    packages=setuptools.find_packages(),
    install_requires=[
        'django', 'djangorestframework >= 3, < 4', 'django-log-request-id'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
