from __future__ import annotations

from re import MULTILINE
from re import search

from setuptools import find_packages
from setuptools import setup


with open("atomic_write_path/__init__.py") as fd:
    version = search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), MULTILINE).group(1)
with open("README.md") as fd:
    long_description = fd.read()
with open("requirements/core.txt") as fd:
    install_requires = fd.read().strip().split("\n")
setup(
    name="atomic-write-path",
    version=version,
    author="Bao Wei",
    author_email="baowei.ur521@gmail.com",
    license="MIT",
    description="Provides the `atomic-write-path` context manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
)
