from setuptools import setup
import pip
import os
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

setup(name='versioned_dictionary',
      version='0.1.1',
      description='A package that provides a class for makeing a full revision history of any dictionary',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://andreacortis@bitbucket.org/andreacortis/versioned_dictionary.git',
      author='Andrea Cortis',
      author_email='andrea.cortis@gmail.com',
      license='MIT',
      packages=['versioned_dictionary'],
      include_package_data=True,
      zip_safe=False,
      install_requires=load_requirements("requirements.txt")
      )
