# -*- coding: utf8 -*-
#
# This file was inspired by: http://github.com/fabiommendes/python-boilerplate/
#

import os

from setuptools import setup, find_packages

# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
path = os.path.join(dirname, 'src', 'ipping', '__meta__.py')
data = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'Krzysztof Błażewicz'
''' % version
with open(path, 'w') as F:
    F.write(data)

setup(
    # Basic info
    name='ipping',
    version=version,
    author='Krzysztof Błażewicz',
    author_email='blazewicz.krzysztof@gmail.com',
    url='https://github.com/blazewicz/ipping-py',
    description='IP (TCP/UDP) ping tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Networking',
        'Typing :: Typed',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='~=3.6',
    install_requires=[
    ],
    extras_require={
        'dev': [
            'flake8',
            'isort',
            'mypy',
        ],
    },

    # Data files
    package_data={
    },

    # Scripts
    entry_points={
        'console_scripts': [
            'ipping = ipping.__main__:main'
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
