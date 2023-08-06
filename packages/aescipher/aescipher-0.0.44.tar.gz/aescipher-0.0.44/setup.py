from setuptools import setup
from importlib import import_module
import os
import re


name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
locals()[name] = import_module(name)
readme = open("README.md").read()
description = re.search(r"<i>(.*?)</i>", readme)[1]
setup(
    name="aescipher",
    version=locals()[name].version,
    keywords=locals()[name].keywords,
    packages=[name],
    url="https://github.com/foxe6-temp/aescipher",
    license="AGPL-3.0",
    author="f̣ộx̣ệ6",
    author_email="foxe6@protonmail.com",
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.7",
    entry_points = dict(console_scripts=[name+"="+name+"."+locals()[name].entry])
)
