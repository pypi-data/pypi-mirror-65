import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lexsub",  # Replace with your own username
    version="1.0.7",
    author="Anish Acharya",
    author_email="anishacharya@utexas.edu",
    description="State of the art Lexical Substitution in Context",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anishacharya/LexSub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')
