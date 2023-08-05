"""setup file for clifold python module"""
from setuptools import find_packages, setup
from clifold.clifold_main import __version__


__version__ = __version__()

tests_require = [
    "pytest",
    "flake8"
]

extras = {
    "test": tests_require
}

setup(
    name="clifold",
    version=__version__,
    author="Jeff Yang",
    author_email="ydc.jeff@gmail.com",
    description="🚀 A CLI tool for scaffolding any Python Projects 🚀",
    # long_description=open("README.md", "r", encoding="utf-8").read(),
    # long_description_content_type="text/markdown",
    keywords="scaffold python project",
    license="MIT",
    url="https://github.com/ydcjeff/clifold",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "clif=clifold.main:cli"
        ],
    },
    install_requires=[
        "requests"
    ],
    extras_require=extras,
    tests_require=tests_require,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities"
    ],
)
