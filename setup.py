import sys
import os
from setuptools import find_packages, setup
from pephubclient import __app_name__, __version__, __author__

PACKAGE = __app_name__
REQDIR = "requirements"

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
def read_reqs(reqs_name):
    deps = []
    with open(os.path.join(REQDIR, f"requirements-{reqs_name}.txt"), "r") as f:
        for l in f:
            if not l.strip():
                continue
            deps.append(l)
    return deps


DEPENDENCIES = read_reqs("all")
extra["install_requires"] = DEPENDENCIES

scripts = None

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
        "Development Status :: 1 - Planing",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="project, bioinformatics, metadata",
    url=f"https://github.com/databio/{PACKAGE}/",
    author=__author__,
    license="BSD2",
    entry_points={
        "console_scripts": [
            "pephubclient = pephubclient.__main__:main",
        ],
    },
    package_data={PACKAGE: ["templates/*"]},
    scripts=scripts,
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra,
)