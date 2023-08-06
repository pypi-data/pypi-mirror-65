"""
This is a setup python file.

This controls the build and packaging to pypi.
For now this is on Peter Mercado's personal pypi.
"""
# Third-Party Libraries
from setuptools import find_packages, setup

setup(
    name="cpaDataServices",
    version="0.0.3",
    python_requires=">=3.6",
    description="CPA data service layer",
    author="Peter Mercado/ CPA",
    author_email="peter.mercado255@gmail.com",
    url="https://github.com/cisagov/cpa/cpa_data_service/services",
    setup_requires=["setuptools-git-version"],
    packages=find_packages(),
    install_requires=["schematics==2.1.0", "pyyaml", "motor==2.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    platforms="any",
    include_package_data=True,
)
