from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pydemy",
    version="0.1.0",
    description="A Python library for interacting with the Udemy Affiliate API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robel Asefa",
    author_email="mertigenet@gmail.com",
    url="https://github.com/robelasefa/pydemy",
    packages=find_packages(),
    install_requires=["requests~=2.32.3", "pydantic~=2.8.2"],
    license='MIT',
)
