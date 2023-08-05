import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="procedure",
    version="0.0.2a",
    author="John Masaon",
    author_email="",
    description="Simple way to use Interactor Pattern in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/binarymason/procedure",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask',
    ],
    python_requires='>=3.6',
)
