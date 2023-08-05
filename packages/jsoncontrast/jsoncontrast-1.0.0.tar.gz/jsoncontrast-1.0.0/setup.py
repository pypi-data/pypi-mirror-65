#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsoncontrast",
    version="1.0.0",
    author="Lijianmei",
    author_email="sophialjm@qq.com",
    description="To contrast two json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sophialjm/jsoncontrast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)