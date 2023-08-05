import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scSplit",
    version="1.0.7",
    author="Jun Xu",
    author_email="jun.xu@uq.edu.au",
    description="Genotype-free demultiplexing of pooled single-cell RNA-Seq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-xu/scSplit",
	packages=setuptools.find_packages(),
	package_data={'': ['scSplit'],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
