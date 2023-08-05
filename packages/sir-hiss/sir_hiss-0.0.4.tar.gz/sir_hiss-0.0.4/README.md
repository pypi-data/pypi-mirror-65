# Sir Hiss

Automatically run the relevant tool (pylint, mypy, pytest, ...) for the current repository.

Tools are detected by peeking at configuration files (pyproject.toml, .pylintrc, ...).

## Usage

From the root of a python project: 

* `hiss` will run the tools
* `hiss --check` prevent the files to be modified by formatters
* `hiss --fast` will skip slowest tools (mostly tests)
* `hiss --preview` will print the list of tools found in the repository


## Why this (stupid) name

Sir Hiss is the name of the snake in "Robin Hood" animated movie.
He has a lot of interesting advice to give to the king but he is never listened to ...
I hope you don't treat your linter like that ^^


## Supported tools

* black
* flake
* isort
* mypy
* nosetest
* pylint
* pytest

Please suggest more tools :-)


## TODO

- Read requirements.txt
- Decide if we should try to read tox.ini. Tox also allow to launch several tools in diferrent environments and there is some overlap with hiss.
- Add installation instructions


## To consider

- Display diff on failure
- Share some options
