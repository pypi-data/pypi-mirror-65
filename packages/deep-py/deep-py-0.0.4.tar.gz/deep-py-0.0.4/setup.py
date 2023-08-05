import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep-py",
    version="0.0.4",
    author="Ruslan Andrusyak",
    description="Python library for Data Science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrusyak/deep-py.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
