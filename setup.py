import os
import sys

from setuptools import setup

from pephubclient import __app_name__, __author__, __version__

PACKAGE = __app_name__
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
    version=__version__,
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
        "Topic :: Scientific/Engineering :: Bioinformatics",
    ],
    keywords="project, bioinformatics, metadata",
    url=f"https://github.com/databio/{PACKAGE}/",
    author=__author__,
    license="BSD2",
    entry_points={
        "console_scripts": [
            "phc = pephubclient.__main__:main",
        ],
    },
    package_data={PACKAGE: ["templates/*"]},
    scripts=None,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra,
)
