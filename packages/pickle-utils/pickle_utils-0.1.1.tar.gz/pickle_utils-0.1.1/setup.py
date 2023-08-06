import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pickle_utils",
    version="0.1.1",
    author="Adrià Garriga-Alonso",
    author_email="adria.garriga@gmail.com",
    description="Memoize functions to disk, load and save compressed Pickle files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/pickle_utils/",
    packages=["pickle_utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas>=1.0"],
    download_url="https://github.com/rhaps0dy/pickle_utils/archive/0.1.1.tar.gz",
    keywords=["pickle"],  # arbitrary keywords
)
