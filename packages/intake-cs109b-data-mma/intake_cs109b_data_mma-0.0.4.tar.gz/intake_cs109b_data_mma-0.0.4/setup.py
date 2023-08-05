#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="intake_cs109b_data_mma",
    version="0.0.4",
    description="Data for cs109b group project, Spring2020",
    py_modules=["intake_cs109b_data_mma"],
    packages=find_packages(),
    package_data={"": ["*.yaml"]},
    include_package_data=True,
    install_requires=["intake", "intake-nested-yaml-catalog"],
    zip_safe=False,
    entry_points={
        "intake.catalogs": [
            "cs109b = intake_cs109b_data_mma:cat",
            "airpred_clean = intake_cs109b_data_mma:data",
        ]
    },
)
