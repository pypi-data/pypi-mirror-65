# ez_pydocs

## Description
ez_pydocs allows you to easily generate documentation for all of your python
files by just providing it your source directory. It generates the documentation
from all doc strings and will render markdown. After it's completed, it provides
you markdown to put into your README.

## Goals
- [ ] Make documentation generation in python ez.
- [ ] Open source this utility.
- [ ] Expand on some features.

## How to run/setup
### Installing via source
```sh
cd ez_pydocs
pip3 install -e . --user
```

```sh
pip3 install ez_pydocs --user
```

It's that ez.

## Usage
```
usage: ez_pydocs.py [-h] directory

positional arguments:
  directory   The directory to traverse. Ideally should be in the same
              directory as your README.md

optional arguments:
  -h, --help  show this help message and exit
```

## How to contribute
Fork the current repository and then make the changes that you'd like to said fork. Upon adding features, fixing bugs,
or whatever modifications you've made to the project, issue a pull request to this repository containing the changes that you've made
and I will evaluate them before taking further action. This process may take anywhere from 3-7 days depending on the scope of the changes made, 
my schedule, and any other variable factors.

## Resources
[pydoc-markdown](https://pypi.org/project/pydoc-markdown/)
