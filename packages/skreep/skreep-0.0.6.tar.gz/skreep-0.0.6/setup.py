import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skreep",
    version="0.0.6",
    author="Korud",
    author_email="khorud@yahoo.com",
    description="Data scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khorud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires= ['selenium'],
    python_requires= '>=3',
)