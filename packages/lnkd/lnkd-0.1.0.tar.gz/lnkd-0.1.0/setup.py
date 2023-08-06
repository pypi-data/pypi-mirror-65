from setuptools import Extension, setup, find_packages

setup(
    name="lnkd",
    version="0.1.0",
    description="Apogee",
    author="Mark Douthwaite",
    author_email="mark.douthwaite@peak.ai",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=["requests", "pyyaml"],
    include_package_data=True,
)