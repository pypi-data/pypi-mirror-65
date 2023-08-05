#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages
from codecs import open

from semres import __version__

# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="semres-jerivas",
    version=__version__,
    description="Testing PyPI and semantic release",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerivas/semres-jerivas",
    author="Unplug Studio",
    author_email="hello@unplug.studio",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="semantic release",
    packages=find_packages(),
    install_requires=[],
    extras_require={"testing": ["flake8>=3,<4", "pytest>=4,<6"]},
    include_package_data=True,
)
