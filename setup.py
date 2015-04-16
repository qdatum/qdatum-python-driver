#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="qdatum",
    version="0.0.2",
    description="API wrapper for the qdatum platform",
    long_description=open("README.md").read(),
    url="https://github.com/qdatum/qdatum-python-driver",
    author="Itamar Maltz",
    author_email="ism@qdatum.io",
    packages=find_packages(),
    install_requires=['requests', 'msgpack'],
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
