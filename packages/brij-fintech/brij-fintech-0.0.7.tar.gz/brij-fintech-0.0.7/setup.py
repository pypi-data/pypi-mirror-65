import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brij-fintech",
    version="0.0.7",
    author="Brian Muigai",
    author_email="brianmuigai1@gmail.com",
    description="A library for brij fintech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brianmuigai/brij",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)