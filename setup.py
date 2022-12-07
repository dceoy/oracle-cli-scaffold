#!/usr/bin/env python

from setuptools import find_packages, setup

version = None

with open('pdoracle.py', 'r') as f:
    for s in f.readlines:
        if s.startswith('__version__ = '):
            version = s.strip().split(' ')[2][1:-1]
            break

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pdoracle',
    version=version,
    author='dceoy',
    author_email='dnarsil+github@gmail.com',
    description='Pandas-based SQL Executor for Oracle DB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dceoy/pdoracle.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['cx_Oracle', 'pandas'],
    entry_points={
        'console_scripts': ['pdoracle=pdoracle:main']
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
