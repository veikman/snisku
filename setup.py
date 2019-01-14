"""Native Python package build instructions."""

from setuptools import setup
from setuptools import find_packages

import snisku

setup(name=snisku.__name__,
      version=snisku.__version__,
      author='Viktor Eikman',
      author_email='viktor.eikman@gmail.com',
      url='viktor.eikman.se',
      description='Application parameter framework',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      packages=find_packages(),
      )
