#!/usr/bin/env python
from setuptools import find_packages, setup
from mlip import __version__


def get_requirements_list(file):
    requirements = []
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            requirements.append(line)
    return requirements


requirements = get_requirements_list("requirements.txt")

setup(
    name="mlip",
    # entry_points=dict(console_scripts=["pipeline-cli=app.main:main"]),
    version=__version__,
    description="Pipeline for images.",
    author="Andre Castro",
    author_email="andreluizfc1@gmail.com",
    url="https://github.com/Andreluizfc",
    packages=find_packages(),
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-flake8", "pytest-cov"],
)
