[![Build Status](https://travis-ci.com/DanielSolomon/coollect.svg?branch=main)](https://travis-ci.com/DanielSolomon/coollect)
[![Coverage Status](https://coveralls.io/repos/github/DanielSolomon/coollect/badge.svg)](https://coveralls.io/github/DanielSolomon/coollect)

COOLLECT
========

Collects functions easily.

## Installing
Tested on CPython 3.6, 3.7, 3.8 and 3.9.

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):
```bash
$ pip install coollect
```

## Description

The `Coollector` package exposes a `Collector` object the collects functions into an organized data structure following a specific `Strategy`. Each collected function is tagged and then can be accessed by querying the `Collector` object for this tag.

### Strategy
`Coollector` supports several collecting *strategies*, the selected strategy determine how functions will be collected:

1. `SINGLE` - A tag can be assigned to a single function only and collecting another function with the same tag will raise an exception.
2. `SINGLE_OVERRIDE` - A tag can be assigned to a single function only and collecting another function with the same tag will replace the current collected function.
3. `MULTIPLE` - Multiple functions can be tagged with the same tag - collection order is not guaranteed.
4. `MULTIPLE_ORDERED` - Multiple functions can be tagged with the same tag - collection order is guaranteed.

## Usage

```python
>>> import coollect
>>> collector = coollect.Collector(strategy=coollect.Strategy.SINGLE)
>>> @collector.collect(tag='first tag')
... def foo():
...  print('foo')
...
>>> # If tag is missing, tag will be the collected function name.
>>> @collector.collect
... def bar():
...  print('bar')
...
>>> collector.get('bar')()
bar
>>> collector.get('first tag')()
foo
>>> # Querying unknown tag will result in `None`.
>>> collector.get('inexistence tag')
>>> 
```