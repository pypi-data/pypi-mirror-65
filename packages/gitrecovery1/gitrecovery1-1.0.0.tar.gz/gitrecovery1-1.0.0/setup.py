import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "gitrecovery1",
    version = "1.0.0",
    author = "Ajayi Praise",
    author_email = "praiseajayi2@gmail.com",
    description = "Help recover git deleted files ",
    long_description =long_description,
    long_description_conten_type = "text/markdown",
    url = "https://github.com/NerdPraise/gitrecoveryfile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)