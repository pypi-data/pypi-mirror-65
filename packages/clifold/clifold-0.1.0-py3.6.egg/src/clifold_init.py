'''Setup file for python project.'''
import os
import getpass
import requests


def py_init(init, project_path, pname):
    '''
    Setup file creation function.

    Args:
        init: True or False
        project_path: initialize setup.py in project directory

    Returns:
        Initialize successful or not
    '''
    template = '''"""setup file for the python project"""
from setuptools import find_packages, setup

setup(
    version="0.1.0",
    author_email="",
    description="",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="",
    license="",
    url="",
    package_dir={},
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    extras_require="",
    tests_require="",
    python_requires=">=3.6.0",
    classifiers=[],
'''
    name, user = pname, getpass.getuser()
    inputs = [template, f'    name="{name}",\n', f'    author="{user}"\n)\n']

    os.chdir(project_path)
    open('README.md', 'w').close()
    print("\n📄 Created README.md...")

    gitig = requests.get(
        'https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore')
    with open('.gitignore', 'wb') as gig:
        for chunk in gitig.iter_content():
            gig.write(chunk)
        gig.close()
    print("\n🚀 Fetched .gitignore from GitHub...")

    if init:
        for i in range(len(inputs)):
            with open('setup.py', 'a+') as setup:
                setup.write(inputs[i])
                setup.close()
        print("\n✨ Generated setup.py...")
    else:
        print("No setup.py created...")
