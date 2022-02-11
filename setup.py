# encoding: utf-8
"""

"""
__author__ = 'Rhys Evans'
__date__ = '27 Jan 2022'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'rhys.r.evans@stfc.ac.uk'

from setuptools import find_namespace_packages, setup

with open("README.md") as readme_file:
    _long_description = readme_file.read()

setup(
    name='stac_fastapi_asset_search',
    description='Asset search extension for STAC. '
                'Developed for use with the stac-fastapi framework',
    author='Rhys Evans',
    url='https://github.com/cedadev/stac-asset-search-ext',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See LICENSE file for details',
    packages=find_namespace_packages(),
    python_requires='>=3.5',
    install_requires=[
        'attr',
        'fastapi',
        'pydantic',
        'typing-extensions',
        'stac-fastapi.api',
        'stac-fastapi.extensions',
        'stac-fastapi.types',
    ],
    extras_require={
        'dev': [
            'pre-commit'
        ]
    }
)
