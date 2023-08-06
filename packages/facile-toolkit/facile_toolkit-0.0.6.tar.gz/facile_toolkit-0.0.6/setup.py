import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facile_toolkit",
    version="0.0.6",
    author="Andrea Gubellini",
    author_email="agubellini@yahoo.com",
    description="A robotframework keywords toolkit used by Facile.it ",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://www.facile.it",
    packages=["faciletoolkit"],
    install_requires=['robotframework', 'robotframework-seleniumlibrary'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)