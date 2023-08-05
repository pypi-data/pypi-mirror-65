#!/usr/local/bin/python3
from setuptools import setup, find_packages
import re
import os

HERE = os.path.dirname(__file__)

def read(fname):
    return open(os.path.join(HERE, fname)).read()


try:
    VERSION = re.search(
        r"__version__\s*=\s*['\"]([^'\"]+)['\"]",
        read("ecotool/_version.py"),
    ).group(1)
except Exception:
    raise RuntimeError("Failed to parse version string")


setup(
    name="ecotool",
    version=VERSION,
    author="chenjiahui",
    author_email="chenjiahui1991@163.com",
    description=("Tools for Economic Applications"),
    license="MIT Licence",
    packages=find_packages(include=("ecotool*", )),
    install_requires=[
    ],
    long_description=read('README.md'),
    include_package_data=False,
)

# vim: ts=4 sw=4 sts=4 expandtab
