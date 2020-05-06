import re

from setuptools import setup

with open("PyBro/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="PyBro",
    version=version,
    install_requires=[
        "wxPython==4.1.0"
    ]
)
