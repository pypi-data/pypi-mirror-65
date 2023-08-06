[![](https://img.shields.io/pypi/v/foliantcontrib.utils.chapters.svg)](https://pypi.org/project/foliantcontrib.utils.combined-options/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.utils.chapters.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.utils.chapters)

# Chapters utils

This module contains utils which make work with Foliant chapter lists easier.

## Installation

To use functions and classes from this module, install it with command

```bash
pip3 install foliantcontrib.utils.chapters
```

## Usage

Right now this module offers only one useful class, called `Chapters`. To start using it, import it:

```python
>>> from foliant.contrib.chapters import Chapters

```

Let's assume we have the following list of chapters specified in foliant.yml:

```yml
chapters:
    - introduction.md
    - Overview:
        - The Problem: problem.md
        - Requirements: req.md
        - Quick Start:
            - qs/installation.md
            - qs/first_steps.md
            - qs/advanced_usage.md
    - Specifications:
        - specs/core.md
        - specs/classes.md
```

If we want to interact wit this list of chapters, we will probably only need path to Markdown-files in the proper order. That's exactly what the `Chapters` class offers. Let's translate this chapter list into Python and give it to the `Chapters` class:

```python
>>> chapters_list = ['introduction.md',{'Overview': [{'The Problem': 'problem.md'},{'Requirements': 'req.md'},{'Quick Start': ['qs/installation.md','qs/first_steps.md','qs/advanced_usage.md']}]},{'Specifications': ['specs/core.md', 'specs/classes.md']}]
>>> chapters = Chapters(chapters_list)

```

### The **flat** property

The `flat` property of the `Chapters` class contains the list of chapter filenames in the correct order, with all the original hierarchy neatly flattened.

```python
>>> for chapter in chapters.flat:
...     print(chapter)
introduction.md
problem.md
req.md
qs/installation.md
qs/first_steps.md
qs/advanced_usage.md
specs/core.md
specs/classes.md

```

### The **paths** method

Usually when we work with chapters, we need not just ther names, as they stated in foliant.yml, but the paths to the actual files.

This is the work of the `paths` method, which accepts one argument: root of the markdown-files directory (usually `src` or `__folianttmp__`).

This method returns a generator, which yields `PosixPath` objects to each chapter in the proper order

```python
>>> for path in chapters.paths('src'):
...     print(repr(path))
PosixPath('src/introduction.md')
PosixPath('src/problem.md')
PosixPath('src/req.md')
PosixPath('src/qs/installation.md')
PosixPath('src/qs/first_steps.md')
PosixPath('src/qs/advanced_usage.md')
PosixPath('src/specs/core.md')
PosixPath('src/specs/classes.md')

```

## Alternative usage

You can also use the `Chapters` object as if it was list:

```python
>>> chapters[0]
'introduction.md'
>>> 'req.md' in chapters
True
>>> for chapter in chapters:
...     print(chapter)
...     break
introduction.md

```

Original chapters list is available in the `chapters` property:

```python
>>> chapters.chapters
['introduction.md', {'Overview': [{'The Problem': 'problem.md'}, {'Requirements': 'req.md'}, {'Quick Start': ['qs/installation.md', 'qs/first_steps.md', 'qs/advanced_usage.md']}]}, {'Specifications': ['specs/core.md', 'specs/classes.md']}]

```

You can redefine your chapters on the fly:

```python
>>> chapters.chapters = ['one.md', {'two': 'three.md'}]
>>> for chapter in chapters:
...     print(chapter)
one.md
three.md

```
