#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='en2cn',
    version=0.10,
    description=(
        '英文翻译到中文的包'
    ),
    #long_description=open('README.rst').read(),
    author='pebble',
    author_email='pebble329@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/pebble329/en2cn-',
    #scripts=["中文词典.py"],
    install_requires = ["re"],  
    include_package_data=True,  
)
