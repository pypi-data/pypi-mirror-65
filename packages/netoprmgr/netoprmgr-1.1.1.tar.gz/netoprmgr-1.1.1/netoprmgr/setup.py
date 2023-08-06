from setuptools import setup
from setuptools import find_packages
import os
import re


with open("README.md", "r") as fs:
    long_description = fs.read()





setup(
    name="netoprmgr",
    version="v1.1",
    description="Project to Manage Network Operation.",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/FunGuardian/netoprmgr",
    author="Funguardian, Dedar, Luthfi",
    author_email="cristiano.ramadhan@gmail.com",
    license="GPLv3+",
    packages=find_packages(exclude=("test*",)),
    install_requires=[
        'netmiko'
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    )
)