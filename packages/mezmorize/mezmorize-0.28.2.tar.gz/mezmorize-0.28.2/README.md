mezmorize
=========

[![travis](https://travis-ci.org/reubano/mezmorize.svg?branch=master)](https://travis-ci.org/reubano/mezmorize)
<!-- [![Coverage Status](https://coveralls.io/repos/reubano/mezmorize/badge.png)](https://coveralls.io/r/reubano/mezmorize) -->
[![versions](https://img.shields.io/pypi/pyversions/mezmorize.svg)](https://pypi.python.org/pypi/mezmorize)
[![pypi](https://img.shields.io/pypi/v/mezmorize.svg)](https://pypi.python.org/pypi/mezmorize)
<!-- [![Documentation Status](https://readthedocs.org/projects/mezmorize/badge/?version=latest)](https://mezmorize.readthedocs.io/en/latest/?badge=latest) -->
[![license](https://img.shields.io/badge/license-BSD-yellow.svg)](https://github.com/reubano/mezmorize)
<!-- [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) -->

A python function memoization library heavily inspired by Flask-Cache.

This is a fork of the [Flask-Cache](https://github.com/thadeusb/flask-cache) extension.

Setup
-----

mezmorize is available on PyPI and can be installed with:

    pip install mezmorize

Usage
-----

```python
from random import randrange

from mezmorize import Cache

cache = Cache(CACHE_TYPE='simple')


@cache.memoize(60)
def add(a, b):
    return a + b + randrange(0, 1000)

# Initial
add(2, 5)

# Memoized
add(2, 5)
add(2, 5)

# Delete cache
cache.delete_memoized(add)

# Initial
add(2, 5)
```

For more configuration options, check out the the [examples](https://github.com/reubano/mezmorize/blob/master/examples/hello.py) or [Flask-Caching documentation](https://flask-caching.readthedocs.io).

Compatibility with Flask-Cache and Flask-Caching
-----
There are no known incompatibilities or breaking changes between either the latest [Flask-Cache v0.13](https://github.com/thadeusb/flask-cache)
or [Flask-Caching v1.8.0](https://github.com/sh4nks/flask-caching) and the current version of mezmorize.

Python versions
-----

Starting with version 0.26.0, mezmorize dropped Python 2 support. The library is tested against Python 3.6, 3.7, 3.8, and PyPy 3.6.

Environment Variables
---------------------
- *CACHE_DIR*: the directory your cache will be stored in. The default is the `cache` dir in the current folder.

Links
=====

* [Flask-Caching Documentation](https://flask-caching.readthedocs.io)
* [Source Code](https://github.com/reubano/mezmorize)
* [Issues](https://github.com/reubano/mezmorize/issues)
* [Current Flask-Caching Extension](https://github.com/sh4nks/flask-caching)
* [Original Flask-Cache Extension](https://github.com/thadeusb/flask-cache)
