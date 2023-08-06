import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terbine-py-library", 
    version="1.0.0",
    author="Jenal Sanchez",
    author_email="jenal@terbine.com",
    description="Python modules used to connect to Terbine's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://terbine.com/specifications/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)