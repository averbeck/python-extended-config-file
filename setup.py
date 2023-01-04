#!/usr/bin/env python3
"""
file-config library
"""

from setuptools import setup, find_packages

setup(
    name="file-config",
    author="Marc Averbeck",
    author_email="ghostcode1337@gmx.com",
    description="Simple configparser wrapper",
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    license_files=('LICENSE',),
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    setup_requires=["setuptools_scm"],
    use_scm_version=True
)
