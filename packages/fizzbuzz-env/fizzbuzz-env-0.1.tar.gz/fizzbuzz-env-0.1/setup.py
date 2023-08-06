import setuptools

long_desc = open("README.md", "r").read()

setuptools.setup(
    name="fizzbuzz-env",
    version="0.1",
    author="Red",
    description="have a script play a game of fizzbuzz",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/TRedRaven/fizzbuzz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
