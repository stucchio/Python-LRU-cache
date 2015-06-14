# Introduction

It's often useful to have an in-memory cache. Of course, it's also desirable not to have the cache grow too large, and cache expiration is often desirable.

This module provides such a cache.

For the most part, you can just use it like this:

```python
from lru import lru_cache_function

@lru_cache_function(max_size=1024, expiration=15*60)
def f(x):
    print "Calling f(" + str(x) + ")"
    return x

f(3) # This will print "Calling f(3)", will return 3
f(3) # This will not print anything, but will return 3 (unless 15 minutes have passed between the first and second function call).
```

One can also create an `LRUCacheDict` object, which is a python dictionary with LRU eviction semantics:

```python
d = LRUCacheDict(max_size=3, expiration=3)
d['foo'] = 'bar'
print d['foo'] # prints "bar"

import time
time.sleep(4) # 4 seconds > 3 second cache expiry of d
print d['foo'] # KeyError
```

In order to configure the decorator in a more detailed manner, or share a cache across fnuctions, one can create a cache and pass it in as an argument to the cached function decorator:

```python
d = LRUCacheDict(max_size=3, expiration=3, thread_clear=True)

@lru_cache_function(cache=d)
def f(x):
    return x/2
```

The doctests in the code provide more examples.

## Installation

```bash
pip install py_lru_cache
```

## When does cache eviction occur?

By default, this cache will only expire items whenever you poke it - all methods on this class will result in a cleanup.

If the `thread_clear` option is specified, a background thread will clean it up every `thread_clear_min_check seconds`.

If this class must be used in a multithreaded environment, the option `concurrent` should be set to `True`. Note that the cache will always be concurrent if a background cleanup thread is used.

## Usage in Python3

Note that this module should probably not be used in python3 projects, since the [standard library already has one](https://docs.python.org/3/library/functools.html). The only feature this one has which that one lacks is timed eviction.
