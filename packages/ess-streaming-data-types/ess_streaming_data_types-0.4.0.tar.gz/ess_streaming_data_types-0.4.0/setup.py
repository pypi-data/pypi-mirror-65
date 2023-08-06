import os
from setuptools import setup, find_packages

DESCRIPTION = "Python utilities for handling ESS streamed data"

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except Exception as error:
    print(error)
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name="ess_streaming_data_types",
    version="0.4.0",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="ScreamingUdder",
    url="https://github.com/ess-dmsc/python-streaming-data-types",
    license="BSD 2-Clause License",
    packages=find_packages(exclude="tests"),
    install_requires=["flatbuffers", "numpy"],
    extras_requires={"dev": ["flake8", "pre-commit", "pytest", "tox"]},
)
