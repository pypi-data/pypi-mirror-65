#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="aes-sid",
    version="0.0.0",
    description="AES-based Synthetic IDs",
    long_description="Authenticated deterministic encryption for 64-bit integers based on the AES-SIV MRAE construction",
    author="Tony Arcieri",
    author_email="tony@iqlusion.io",
    url="https://github.com/iqlusioninc/aes-sid/blob/develop/README.md",
    packages=["aes-sid"],
    package_dir={"aes-sid": "aes-sid"},
    include_package_data=True,
    install_requires=[],
    license="Apache Software License",
    keywords=["encryption", "signing"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
    ],
    test_suite="tests",
    tests_require=[]
)
