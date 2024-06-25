from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pydemy",
    version="0.1",
    description="A Python library for interacting with the Udemy Affiliate API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robel Asefa",
    author_email="mertigenet@gmail.com",
    maintainer="Robel Asefa",
    maintainer_email="mertigenet@gmail.com",
    url="https://github.com/robelasefa/pydemy",
    packages=find_packages(),
    requires=["requests~=2.32.3", "pydantic~=2.8.2"],
    keywords=["udemy", "api", "courses", "education"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
