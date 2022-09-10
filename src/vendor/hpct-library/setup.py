# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# setup.py

"""Install hpctlib with pip."""

from setuptools import setup, find_packages

setup(
    name="hpctlib",
    version="0.1.0",
    description="Canonical HPC Team's internal library",
    license="Apache-2.0",
    packages=find_packages(
        where="lib",
        include=["hpctlib*"],
    ),
    package_dir={"": "lib"},
    install_requires=["cryptography", "ops"],
    classifiers=[
        "Development State :: 1 - Planning",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
