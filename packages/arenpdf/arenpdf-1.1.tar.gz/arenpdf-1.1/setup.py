import setuptools
from pathlib import Path

setuptools.setup(
    name="arenpdf",
    version=1.1,
    long_description=Path("READMe.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)