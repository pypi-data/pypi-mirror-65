import setuptools
from strongdoc import __version__

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open("README.md", "r") as fh:
    long_description = fh.read() + history

setuptools.setup(
    name="strongsalt-strongdoc-python-sdk",
    version=__version__,
    author="StrongDoc",
    author_email="info@strongsalt.com",
    description="The StrongDoc Python SDK for interacting with the StrongDoc API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/overnest/strongdoc-python-sdk",
    license="LICENSE.txt",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "pathlib",
        "grpcio",
        "protobuf",
        "six"
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
