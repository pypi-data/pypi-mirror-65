import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SPyQR",
    version="0.0.1",
    author="lukekh",
    author_email="groupython@gmail.com",
    description="A bad python package for bad Romans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukekh/SPyQR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
