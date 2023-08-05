import setuptools
from numpy.distutils.core import Extension
from numpy.distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="LoveUpdate",
    version="0.0.1",
    author="Pedro de Almeida Secchi",
    author_email="pedrosecchimail@gmail.com",
    description="Autoupdate package for LovelacePM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrosecchi67/LoveUpdate",
    packages=['LoveUpdate'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'pip-check', 'datetime'],
    python_requires='>=3.6',
)
