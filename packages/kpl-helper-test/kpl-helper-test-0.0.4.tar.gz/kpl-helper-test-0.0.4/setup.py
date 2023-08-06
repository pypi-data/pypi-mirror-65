#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='kpl-helper-test',
      version='0.0.4',
      platforms='any',
      packages=find_packages(),
      install_requires=[
          'requests',
          'flask',
          'flask-cors',
          'PyYAML',
          'kpl-dataset'
      ],
      entry_points={
          "console_scripts": [
              "helper = kpl_helper.parameter:write_parameter",
          ],
      },
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
      ])
