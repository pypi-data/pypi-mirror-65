#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()


setup(name='arts_tools',
      version='1.0',
      description='Tools to read or process ARTS data',
      long_description=readme,
      long_description_content_type="text/markdown",
      url='http://github.com/loostrum/arts_tools',
      author='Leon Oostrum',
      author_email='oostrum@astron.nl',
      license='Apache2.0',
      packages=find_packages(),
      install_requires=['numpy>=1.17'],
      entry_points={'console_scripts': ['arts_fix_fits=arts_tools.fits.fix_file:main']},
      classifiers=['License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3',
                   'Operating System :: OS Independent'],
      python_requires='>=3.6'
      )
