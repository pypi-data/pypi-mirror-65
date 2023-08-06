from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# add packages from requirements
with open(path.join(this_directory, 'requirements.txt'),'r') as f:
    required = f.read().splitlines()

setup(
    name='TemplateGitHub',
    version='0.0.1',
    author='drbmrp',
    author_email='borja.rojo.perez@gmail.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/drbmrp/TemplateGitHub/',
    license='LICENSE.txt',
    description='A package containing a dog',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

)
