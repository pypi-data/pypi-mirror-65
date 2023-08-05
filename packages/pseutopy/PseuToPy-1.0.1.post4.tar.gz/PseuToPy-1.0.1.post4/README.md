[![Build Status](https://travis-ci.com/PatWg/PseuToPy.svg?branch=master)](https://travis-ci.com/PatWg/PseuToPy)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

# PseuToPy

PseuToPy is a Python library which defines a grammar for a pseudocode-based
 pseudocode. With this grammar, PseuToPy is then able to take instructions
  written in pseudocode and convert it into the equivalent Python instructions.

PseuToPy is designed for educational purposes. In that sense, PseuToPy is
 suited to anyone embarking in the journey of learning Python programming by
  offering a relaxed syntax and a grammar that very much resembles the
   grammar of a natural language.
   
Currently, PseuToPy only exists in English, but more languages (French,
 Italian, Spanish) will arrive soon.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PseuToPy.

```shell script
pip install pseutopy
```

This will also install the following dependencies:

- [textX](http://textx.github.io/textX/stable/)
- [astor](https://astor.readthedocs.io/en/latest/)


## Usage

You can import PseuToPy and use it within your own project.

```python
from pseutopy.pseutopy import PseuToPy
import astor

pseutopy = PseuToPy()

# These two lines generate the AST of the pseudocode instructions
convert_from_string = pseutopy.convert_from_string("declare a set a to 3 plus 1")
convert_from_file = pseutopy.convert_from_file("./path/to/file")

# You can then convert these AST into Python instructions with astor
print(astor.to_source(convert_from_string))
print(astor.to_source(convert_from_file))
```

Or you can use the CLI utility that ships with this repository.

```shell script
python pseutopy.py --help

# This is the output of the help flag
usage: pseutopy.py [-h] [-f | -s] [-a] [-q] input

A pseudocode to Python converter written in Python using textX.

positional arguments:
  input         Pseudocode input and to be converted into Python

optional arguments:
  -h, --help    show this help message and exit
  -f, --file    Input is now expected to be a file
  -s, --string  Input is now expected to be a string (default)
  -a, --ast     Prints out the generated Python AST
  -q, --quiet   Don't print the generated Python code
```

 
 ## Testing
 
 To run unit tests, run `pytest` at the root of the project.
 
 
 ## Authors and acknowledgment
 
I particularly wish to thank [@Houguiram](https://github.com/Houguiram
), [@TheOnlyMrFlow](https://github.com/TheOnlyMrFlow), and [@EricSombroek
](https://github.com/EricSombroek) for their contributions which greatly
 helped in setting up the bases for this project.
 
 ## License
 
[MIT](https://choosealicense.com/licenses/mit/)
