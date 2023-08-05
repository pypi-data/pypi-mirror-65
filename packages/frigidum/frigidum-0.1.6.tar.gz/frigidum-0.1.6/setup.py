import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = "0.0.1"

setuptools.setup(
    name="frigidum",
    version=version,
    author="Willem Hendriks",
    author_email="whendrik@gmail.com",
    description="Simmulated Annealing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/whendrik/frigidum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['tqdm>=3.0.0']
)