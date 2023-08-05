from pathlib import Path
import setuptools
setuptools.setup(
    name="photalpdf",
    version=4.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
