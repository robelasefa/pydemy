"""Configure installation for pydemy package."""

from setuptools import find_packages, setup


def get_long_description() -> str:
    """Reads the long description from README.md."""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="pydemy",
    version="0.2.8",
    description="A Python library for interacting with the Udemy Affiliate API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Robel Asefa",
    author_email="mertigenet@gmail.com",
    url="https://github.com/robelasefa/pydemy",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["requests~=2.32.3", "pydantic>=2.9.1,<2.11.0"],
)
