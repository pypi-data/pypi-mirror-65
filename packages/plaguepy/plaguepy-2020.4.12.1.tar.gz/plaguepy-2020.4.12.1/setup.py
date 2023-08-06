import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plaguepy",
    version="2020.04.12.1",
    author="Thijs van den Berg",
    author_email="denbergvanthijs@gmail.com",
    description='Ziekteverspreiding gevisualiseerd',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/denbergvanthijs/plaguepy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
