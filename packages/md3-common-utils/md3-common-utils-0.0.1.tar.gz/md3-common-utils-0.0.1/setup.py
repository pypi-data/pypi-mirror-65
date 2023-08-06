# -*- coding: utf-8 -*-
#
# MD3 common utils
#
# Copyright (C) 2020-2020 Project
# Author: MD3 <dev@md3.pt>
# URL: <https://www.md3.pt/en/>
# For license information, see LICENSE.txt

from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="md3-common-utils",
    description="Common utils",
    version="0.0.1",
    url="https://www.md3.pt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    keywords=["utils"],
    maintainer="MD3",
    maintainer_email="dev@md3.pt",
    author="MD3",
    author_email="dev@md3.pt",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["md3", "md3.common"],
    package_dir={"": "src"},
    data_files=[("", ["LICENSE.txt"]), ("", ["README.md"])],
    python_requires="<=3.6.9,>=2.7",
    install_requires=["Unidecode==1.0.22"]
)
