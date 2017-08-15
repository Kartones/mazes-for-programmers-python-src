# Mazes For Programmers Python Sources

## Introduction

I'm reading the [Mazes for Programmers](http://www.mazesforprogrammers.com) book, but source code comes in Ruby and I like Python, so I decided to rewrite them as I read. And along the way add tests, both to make sure the conversion is ok and to see a more continuous way than having to write all basic stuff and an "ASCII renderer" to see anything.

## Setup

Note: Code is typed using the great library `mypy`.

```
pip install -r requirements.txt
```

## Running

```
> PYTHONPATH=. python3 demos/binary_tree_demo.py
+---+---+---+---+---+---+
|                       |
+---+   +---+---+   +   +
|       |           |   |
+   +   +   +---+---+   +
|   |   |   |           |
+---+   +---+   +   +   +
|       |       |   |   |
+---+   +   +   +---+   +
|       |   |   |       |
+   +   +   +   +---+   +
|   |   |   |   |       |
+---+---+---+---+---+---+

```

Renderers do not share any interface, just a `render()` method which also varies in parameters, as some output to console while others save to a PNG file.


## Testing

Note: Runs also some linter tests, to conform with both `mypy` and `flake8`.

```
pytest
```