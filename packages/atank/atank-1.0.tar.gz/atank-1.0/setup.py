#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='atank',
    version=1.0,
    description=(
        '<项目的简单描述>'
    ),
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='shwangjj',
    author_email='shwangjj@163.com',
    maintainer='shwangjj',
    maintainer_email='shwanjj@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/shwdbd/atank',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)