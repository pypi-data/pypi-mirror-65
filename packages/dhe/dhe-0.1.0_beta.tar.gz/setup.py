#!/usr/bin/env python3
"""
To only compile the C extension inplace:
python setup.py build_ext --inplace
"""

from datetime import datetime
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    raise RuntimeError('setuptools is required')

from setup_helpers import LazyList

pypi_url = 'http://192.168.1.23:10180/packages/'


def load_extensions():
    """ Gets plugged into a LazyList to prevent numpy import until numpy is installed """
    from numpy import get_include as _numpy_get_include
    yield Extension('c_dhe',
                    sources=["dhe/c_dhe/c_dhe.c", "dhe/c_dhe/c_dhe_module.c"],
                    include_dirs=[_numpy_get_include()])
    yield Extension('c_dhe_full',
                    sources=["dhe/c_dhe/c_dhe_full.c",
                             "dhe/c_dhe/c_dhe_full_module.c"],
                    include_dirs=[_numpy_get_include()])


# The following line will be replaced by ci:
VERSION = '{dt.year}.{dt.month}.{dt.day}.dev1'.format(dt=datetime.now())

setup(name="dhe",
      version=VERSION,
      packages=find_packages(),
      description="DHE",
      author='Gerhard Bräunlich',
      author_email='gbraeunlich@s3-engineering.ch',
      url='https://gitlab.s3-engineering.ch/gbraeunlich/dhe',
      download_url=pypi_url,
      dependency_links=[pypi_url],
      keywords=[],
      install_requires=["numpy"],
      setup_requires=[
          'numpy',
          'scipy',
          # 'wxPython'
      ],
      classifiers=[],
      python_requires=">=3.5",
      ext_package="dhe",
      ext_modules=LazyList(load_extensions()),
      scripts=['bin/dhe-cmd'],
      entry_points={
          'console_scripts': ['dhe=dhe.gui:main'],
      }
      )
