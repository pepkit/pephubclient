import os
import sys

from setuptools import setup

with open(os.path.join("pephubclient", "__init__.py")) as f:
    for line in f:
        if line.startswith("__app_name__"):
            PACKAGE = line.split("=")[1].strip().strip('"')
        if line.startswith("__author__"):
            AUTHOR = line.split("=")[1].strip().strip('"')
        if line.startswith("__version__"):
            VERSION = line.split("=")[1].strip().strip('"')

REQDIR = "requirements"

# Additional keyword arguments for setup().
extra = {}


# Ordinary dependencies
def read_reqs(reqs_name):
    with open(os.path.join(REQDIR, f"requirements-{reqs_name}.txt"), "r") as f:
        return [line.strip() for line in f if line.strip()]


extra["install_requires"] = read_reqs("all")

with open("README.md") as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=VERSION,
    description="PEPhub command line interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="project, bioinformatics, metadata",
    url=f"https://github.com/databio/{PACKAGE}/",
    author=AUTHOR,
    author_email="khorosh@virginia.edu",
    license="BSD2",
    entry_points={
        "console_scripts": [
            "phc = pephubclient.__main__:main",
        ],
    },
    package_data={PACKAGE: ["templates/*"]},
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("test"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra,
)
