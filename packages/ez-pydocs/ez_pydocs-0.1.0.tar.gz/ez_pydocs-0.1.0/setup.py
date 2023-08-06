
"""
Setup.py for installing ez_pydocs
"""
import pathlib

from setuptools import find_packages, setup

# Get the directory that this file is in
DIR = pathlib.Path(__file__).parent

# Read the text of the markdown file
README = (DIR / "README.md").read_text()

# Setup the pip package
setup(
    name="ez_pydocs",
    version="0.1.0",
    description="Generating python documentation made ez.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/codingclaw/ez_pydocs",
    author="C3NZ",
    author_email="cenz@cenz.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=["wheel"],
    install_requires=[
        "pydoc-markdown==2.1.3"
    ],
    entry_points={"console_scripts": ["ez_pydocs=src.ez_pydocs:main"]},
)
