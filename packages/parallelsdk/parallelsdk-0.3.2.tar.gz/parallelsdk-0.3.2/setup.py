# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='parallelsdk',
    version='0.3.2',
    description='Parallel AI Frontend Python SDK',
    author='Austin Garrett',
    author_email='agarrett777@gmail.com',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires = requirements
)
