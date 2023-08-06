# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    readme = f.read()

setup(
        name="argunizer",
        version="0.1.0",
        description="Argunizer is a tool for creating and maintaining temporal hierarchies.",
        long_description=readme,
        long_description_content_type="text/x-rst",
        author="Lari Huttunen",
        author_email="mitcode@huttu.net",
        url="https://gitlab.com/svimes/argunizer",
        packages=find_packages(exclude=("tests")),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
    )
