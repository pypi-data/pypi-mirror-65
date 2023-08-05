import setuptools
import sys
from glob import glob

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="amle-py", # Replace with your own username
    version="1.1.1",
    author="Theo De castro Pinto",
    author_email="decastrotheo960@gmail.com",
    description="A package that can be used to make an AI learn from Amstrad CPC games.",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        "amle_py": ["data/rom/*", 
                    "data/resources/*.*", 
                    "data/resources/freedesktop/*", 
                    "libamle_c.so", 
                    "DLL/32Bit/*",
                    "DLL/64Bit/*",
                    "data/SupportedGames/*"],
    },
    include_package_data=True,
)