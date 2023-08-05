#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='kpl-dataset-test',
      version='0.0.3',
      platforms='any',
      description='KPL Dataset',
      packages=find_packages(),
      install_requires=[
          'protobuf==3.11.0'
      ],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
