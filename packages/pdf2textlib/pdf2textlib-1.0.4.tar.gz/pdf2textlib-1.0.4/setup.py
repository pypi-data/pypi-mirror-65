import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdf2textlib", # Replace with your own username
    version="1.0.4",
    author="Vedant Khairnar",
    author_email="vedron007@gmail.com",
    description="A package to extract text from PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FSOCIETY06/pdf2textlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
