#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

setup(name = 'eupy',
      version = '0.0.5',
      description = 'Python set of utils and libraries',
      url = 'http://github.com/fivosts/eupy',
      author = 'Foivos Tsimpourlas',
      author_email = 'fivos_ts@hotmail.com',
      license = 'MIT',
      install_requires = [ "datetime",
                           "matplotlib",
                           "numpy",
                           "scrapy>=2.0.0",
                           "seaborn",
                           "pathlib",
                        ],
      # package_dir = {'hermes'   : 'eupy/hermes',
      #                'mrcrawley': 'eupy/mrcrawley',
      #                'native'   : 'eupy/native',
      #               },
      # packages = ['eupy.mrcrawley', 'eupy.native', 'eupy.hermes'],
      packages = ["eupy"],
      classifiers = [
           "Programming Language :: Python :: 3.7",
      ]
      )
