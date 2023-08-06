#!/usr/bin/env python

from distutils.core import setup

setup(
    name="disqusting",
    version="0.02",
    description="Very simple (and incomplete) library for Disqus API",
    url="https://github.com/vanatteveldt/disqusting",
    author="Wouter van Atteveldt",
    author_email="wouter@vanatteveldt.com",
    packages=["disqusting"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "requests",
    ]
)
