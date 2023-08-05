import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frigidum",
    version="0.0.3",
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
)