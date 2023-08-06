from setuptools import find_packages, setup

import mpp.main


with open("README.md") as f:
    long_description = f.read()

setup(
    name="mpp",
    version=mpp.main.__version__,
    author="deplanty",
    description="My Python Project: a command-line tool to create a Pythpn project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deplanty/mpp",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mpp = mpp.main:main",
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires=">=3.7"
)
