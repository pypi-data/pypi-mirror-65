import fnmatch
from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as build_py_orig

with open("description_pypi.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="Grimsel",
    version="0.8.19",
    author="Grimsel contributors listed in AUTHORS",
    author_email="mcsoini_dev@posteo.org",
    description=("GeneRal Integrated Modeling environment for the Supply of"
                 " Electricity and Low-temperature heat"),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mcsoini/grimsel",
    packages=find_packages(),
 #   install_requires=['pyutilib', 'pandas', 'Pyomo',
 #                     'wrapt', 'psycopg2', 'numpy'
 #                     ],
    install_requires=[
        "bottleneck >= 1.2",
        "click >= 7, < 8",
        "ipython >= 7",
        "ipdb >= 0.11",
        "jinja2 >= 2.10",
        "natsort >= 5",
        "netcdf4 >= 1.2.2",
        "numexpr >= 2.3.1",
        "numpy >= 1.15",
        "pandas >= 0.25, < 0.26",
        "plotly >= 3.3, < 4.0",
        "pyomo >= 5.6, < 5.7",
        "ruamel.yaml >= 0.16",
        "scikit-learn >= 0.22",
        "xarray >= 0.14, < 0.15",
    ],    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"],
)

