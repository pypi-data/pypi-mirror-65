#!/usr/bin/env python

from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup

VERSION = ""
DESCRIPTION = """
Robot Framework keyword library wrapper around the HTTP client library requests.
"""[1:-1]

CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

version_file = join(dirname(abspath(__file__)), 'src', 'RequestsExtension', 'version.py')

with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

setup(name='robotframework-requests-extension',
      version=VERSION,
      description='RequestsLibrary Extension',
      long_description=DESCRIPTION,
      author='Vincenzo Gasparo',
      author_email='vincenzo.gasparo@gmail.it',
      maintainer='Vincenzo Gasparo',
      maintainer_email='vincenzo.gasparo@gmail.it',
      url='',
      license='MIT',
      keywords='robotframework testing test automation http client requests',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['RequestsExtension'],
      install_requires=[
          'robotframework',
          'robotframework-requests',
          'requests', 
          'jsonschema'
      ]
      )

""" Official release from master
# make sure the setup version has been increased
"""
