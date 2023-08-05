import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XivDbReader", # Replace with your own username
    version="0.0.1",
    author="James Tombleson",
    author_email="jtombleson38@gmail.com",
    description="Web scraping package to read the Final Fantasy XIV DB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luther38/XivDbReader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)