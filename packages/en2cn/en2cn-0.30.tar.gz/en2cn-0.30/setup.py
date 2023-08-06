#!/usr/bin/env python
# coding=utf-8

'''
from setuptools import setup, find_packages

__all__ = ['中文词典', '翻译', '词典数据']
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
'''

import setuptools

with open("README.md", "r" , encoding = 'utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="en2cn", # Replace with your own username
    version="0.30",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    #package_dir = {'': 'en2cn'},
	include_package_data=True,
    package_data={'en2cn': ['词典数据/*.ts']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)