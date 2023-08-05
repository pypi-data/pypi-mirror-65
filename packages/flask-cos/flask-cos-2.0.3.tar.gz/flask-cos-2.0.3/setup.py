#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.rst") as f:
    readme = f.read()


setup(
    name="flask-cos",
    version="2.0.3",
    description="腾讯云对象存储的Flask扩展",
    long_description=readme,
    author="codeif",
    author_email="me@codeif.com",
    url="https://github.com/codeif/flask-cos",
    license="MIT",
    install_requires=["qcos>=2.0"],
    packages=find_packages(exclude=("tests", "tests.*")),
)
