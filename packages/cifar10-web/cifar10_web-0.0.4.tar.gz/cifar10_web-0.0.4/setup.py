import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cifar10_web", 
    version="0.0.4",
    author="QData",
    author_email="jm8wx@virginia.edu",
    description="A package for obtaining data from CIFAR10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QData/cifar10_web",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
