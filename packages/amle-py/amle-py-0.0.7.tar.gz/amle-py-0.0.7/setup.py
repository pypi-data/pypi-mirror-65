import setuptools
import sys
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amle-py", # Replace with your own username
    version="0.0.7",
    author="Theo De castro Pinto",
    author_email="decastrotheo960@gmail.com",
    description="A package that can be used to make an AI learn from Amstrad CPC games.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
                    "amle_c.dll",
                    "data/SupportedGames/*"],
    },
    include_package_data=True,
)