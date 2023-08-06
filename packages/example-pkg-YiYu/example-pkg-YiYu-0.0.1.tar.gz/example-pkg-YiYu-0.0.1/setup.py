import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "example-pkg-YiYu",   # package name
    version = "0.0.1",
    author = "Yi Yu",
    author_email = "q1499114179@gmail.com",
    description = "This is a simple example package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    package = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">= 3.6",
)