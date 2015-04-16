#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="qdatum-api",
    version="0.0.1",
    description="API wrapper for the qdatum platform",
    long_description=open("README.rst").read(),
    url="https://github.com/ism-qdatum/qdatum-api-python",
    author="Itamar Maltz",
    author_email="ism@qdatum.io",
    packages=find_packages(),
    install_requires=['requests'],
    platforms=["any"],
    license='MIT',
    keywords="qdatum api",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
)
