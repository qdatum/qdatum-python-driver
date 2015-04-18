#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="qdatum",
    version="0.0.5",
    description="API wrapper for the qdatum platform",
    url="https://github.com/qdatum/qdatum-python-driver",
    download_url='https://github.com/qdatum/qdatum-python-driver/tarball/0.0.5',
    author="Itamar Maltz",
    author_email="ism@qdatum.io",
    packages=find_packages(),
    install_requires=['future', 'requests', 'requests-futures', 'msgpack-python'],
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
