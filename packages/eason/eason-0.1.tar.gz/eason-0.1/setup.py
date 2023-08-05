from setuptools import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='eason',
    version='0.01',
    description='A useful python tools package create by EasonC13',
    url='https://github.com/EasonC13/eason',
    author='EasonC13',
    author_email='eason.tw.chen@gmail.com',
    license='MIT',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
    
)
