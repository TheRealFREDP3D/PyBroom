# setup.py
from setuptools import setup

setup(
    name="pybroom",
    version="0.1.0",
    py_modules=["pybroom"],
    entry_points={
        "console_scripts": [
            "pybroom=pybroom:main",
        ],
    },
    install_requires=[],
    author="Frederick Pellerin <fredp3d@proton.me>",
    description="🧹 A Python cleanup tool for removing __pycache__ and virtual environments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)

