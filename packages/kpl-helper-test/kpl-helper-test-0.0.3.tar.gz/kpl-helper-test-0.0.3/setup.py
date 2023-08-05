#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='kpl-helper-test',
      version='0.0.3',
      platforms='any',
      packages=find_packages(),
      install_requires=[
          'requests==2.18.4',
          'flask==1.1.1',
          'flask-cors==3.0.8',
          'PyYAML==3.12',
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
