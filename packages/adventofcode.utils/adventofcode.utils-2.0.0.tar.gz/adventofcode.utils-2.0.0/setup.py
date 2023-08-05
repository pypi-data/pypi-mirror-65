from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='adventofcode.utils',
    version='2.0.0',
    description='Advent of Code utility classes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dh256/adventofcode/tree/master/utils',
    author='David Hanley',
    author_email='hanley_d@hotmail.com',
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)