#!/usr/bin/env python
import os
import sys
from codecs import open
from os import path

from setuptools import setup
from garpundatahub import info

if sys.version_info < (3, 6, 0):
    print("Python 3.6+ is required")
    exit(1)

here = os.path.abspath(os.path.dirname(__file__))

long_description = """The Garpun DataHub API Client for Python is a client library for 
accessing the DataHub user data. Also provides Pandas wrapper class."""

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")]

setup(
    name=info.__package_name__,
    version=info.__version__,
    description="Garpun DataHub API Library for Python",
    long_description=long_description,
    url="https://github.com/garpun/garpun-auth-library-python",
    author="Garpun Cloud",
    author_email="support@garpun.com",
    license="Apache 2.0",
    zip_safe=False,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
    python_requires=">=3.6",
    packages=["garpundatahub"],
    package_data={"": ["LICENSE"]},
    include_package_data=True,
)
