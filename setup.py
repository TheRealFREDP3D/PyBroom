# setup.py
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pybroom",
    version="0.1.2",
    py_modules=["pybroom"],
    entry_points={
        "console_scripts": [
            "pybroom=pybroom:main",
        ],
    },
    install_requires=[],
    author="Frederick Pellerin",
    author_email="fredp3d@proton.me",
    description="🧹 A Python cleanup tool for removing __pycache__ and virtual environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRealFREDP3D/PyBroom",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Systems Administration",
        "Environment :: Console",
    ],
    keywords="python cleanup cli cache virtual-environment build-artifacts development-tools",
    license_files=["LICENSE"],
)

