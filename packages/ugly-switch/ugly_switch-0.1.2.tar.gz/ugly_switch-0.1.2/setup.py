#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-03-20"
__version__ = "0.0.0"

__all__ = ()

from pathlib import Path
from setuptools import setup, find_packages

if __name__ == '__main__':
    with Path('README.md').open('r') as file: long_description = file.read()
    setup(
        name='ugly_switch',
        version='0.1.2',
        packages=find_packages(),
        url='https://github.com/RoW171/ugly_switch',
        license='MIT',
        author=__author__,
        author_email='robin.weiland@gmx.de',
        description='An ugly pseudo solution for using switches in python. ',
        long_description=long_description,
        long_description_content_type='text/markdown',
        keywords=['switch'],
        python_requires='>=3.7',  # due to __class_getitem__  see PEP560
        py_modules=['ugly_switch'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development',  # sort of
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
            'Operating System :: OS Independent',
        ],
    )
