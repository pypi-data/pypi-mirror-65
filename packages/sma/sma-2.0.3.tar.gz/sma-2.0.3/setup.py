#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sma",
    version="2.0.3",
    author="Tim Seppelt",
    author_email="t.seppelt-dev@posteo.de",
    description="Package for analysing social-ecological networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/t.seppelt/sesmotifanalyser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "networkx",
        "numpy",
        "scipy",
        "pandas",
        "matplotlib"
    ]
)