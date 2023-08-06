"""A setuptools based setup module for eyap

Copyright (c) 2017, Emin Martinian
See LICENSE at the top-level of this distribution for more information
or write to emin.martinian@gmail.com for more information.
"""

from os import path
from setuptools import setup, find_packages


def get_readme():
    'Get the long description from the README file'

    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst'), encoding='utf-8') as my_fd:
        result = my_fd.read()

    return result

setup(
    name='eyap',      # version is below not in eyap.__init__ since init
    version='0.9.2',  # needs dependancies already installed for import
    description='Tools for extending yapping and comment management',
    long_description=get_readme(),
    url='http://github.com/emin63/eyap',
    author='Emin Martinian',
    author_email='emin.martinian@gmail.com',
    license='custom',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='comment management',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests', 'python-dateutil'],
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        'sample': ['package_data.dat'],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
