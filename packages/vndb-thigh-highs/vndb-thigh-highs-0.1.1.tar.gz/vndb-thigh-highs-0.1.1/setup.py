#!/bin/env python

import setuptools

with open("README.md") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="vndb-thigh-highs",
    version="0.1.1",
    author="foiegras",
    author_email="le.tortue@tutanota.com",
    description="VNDB api client implementation and dumps helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.blicky.net/FoieGras/vndb-thigh-highs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
