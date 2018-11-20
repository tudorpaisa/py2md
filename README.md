# py2md

`py2md` is a doctring-based convertor from `py` to `md` markdown files

## Usage

```
python ./py2md.py [INPUT] [OUTPUT]
```

## Dependencies

`None`. The script uses Python's built-in `re` module to do the conversion.

## How to

To get a proper output from `py2md`, you delimit the markdown text with doctring, like so...

```python
"""
# Header

This is a piece of text.
"""
```

... and write your code as per-usual...

```python
print("Hello, world!")
```

That's it. You're done :)

## YAML Metadata

`py2md` has partial support for YAML metadata that you can include in your file. This is useful if you want to convert the resulting `md` file to `pdf` using [pandoc](https://pandoc.org/). In a `py` file, the metadata is represented using [module-level dunder names](https://legacy.python.org/dev/peps/pep-0008/#module-level-dunder-names). This approach corresponds to PEP8 conventions.

To illustrate, in a `py` file you write...

```python
__title__ = "Lorem Ipsum"
```

... which results in the following in your `md` file:

```
---
title: "Lorem Ipsum"
---
```

Currently supported YAML metadata keys are:

```
title
author
date
keywords
```

## To-Do

- [ ] Remove module-level dunders from final `md`
- [ ] Add support for other YAML metadata keys
