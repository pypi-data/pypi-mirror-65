#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup

setup(name='eupy',
      version='0.0.1',
      description='Python set of utils and libraries',
      url='http://github.com/fivosts/eupy',
      download_url='https://github.com/fivosts/eupy/archive/0.0.1.tar.gz',
      author='Foivos Tsimpourlas',
      author_email='fivos_ts@hotmail.com',
      license='MIT',
      install_requires = [ "datetime",
                           "matplotlib",
                           "numpy",
                           "scrapy>=2.0.0",
                           "seaborn",
                           "pathlib",
                        ],
      package_dir = {'hermes'   : 'eupy/hermes',
                     'mrcrawley': 'eupy/mrcrawley',
                     'native'   : 'eupy/native',
                    },
      packages=['mrcrawley', 'native', 'hermes'],
      )
