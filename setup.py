"""Configure installation for pydemy package."""

from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def get_long_description() -> str:
    """Reads the long description from README.md."""
    with Path("README.md").open(encoding="utf-8") as f:
        return f.read()


def get_requirements() -> List[str]:
    """Reads requirements from requirements.txt and returns a list of dependencies."""
    with Path("requirements.txt").open() as requirements:
        return [line.strip() for line in requirements]


setup(
    name="pydemy",
    version="0.1.1",
    description="A Python library for interacting with the Udemy Affiliate API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Robel Asefa",
    author_email="mertigenet@gmail.com",
    url="https://github.com/robelasefa/pydemy",
    packages=find_packages(exclude=["tests*"]),
    install_requires=get_requirements(),
)
