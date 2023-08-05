#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()


setup(
    author='Nicollas Borges',
    author_email='nicollasborges@lojaspompeia.com.br',
    description='Classe para uso da API unous.',
    license='MIT',
    name='lins_unous',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins_unous/',
    version=get_version()
)