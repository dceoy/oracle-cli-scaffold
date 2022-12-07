#!/usr/bin/env python

from setuptools import find_packages, setup

from pdrdb import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pdrdb',
    version=__version__,
    author='dceoy',
    author_email='dnarsil+github@gmail.com',
    description='Pandas-based SQL Executor for RDBMS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dceoy/pdrdb.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['cx_Oracle', 'pandas', 'psycopg2-binary', 'sqlalchemy'],
    entry_points={
        'console_scripts': ['pdrdb=pdrdb.cli:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ],
    python_requires='>=3.6',
)
