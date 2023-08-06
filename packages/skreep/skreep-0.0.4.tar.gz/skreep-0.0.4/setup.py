import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skreep", # Replace with your own username
    version="0.0.4",
    author="Korud",
    author_email="khorud@yahoo.com",
    description="Scraper Lib",
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
    install_requires= ['selenium'],
    python_requires= '>=3',
)