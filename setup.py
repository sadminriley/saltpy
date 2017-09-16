#!/usr/bin/python
from setuptools import setup
# SaltPY setup
setup(
    name = "SaltPY",
    version = "0.1",
    author = "Riley",
    author_email = "riley@fasterdevops.com",
    url = "https://github.com/sadminriley/",
    license = "MIT",
    install_requires=[
        "saltpy==0.1"
        "paramiko==2.2.1"
    ],
    dependency_links=[
        "git+https://github.com/sadminriley/saltpy.git#egg=saltpy-0.1"
    ]
)
