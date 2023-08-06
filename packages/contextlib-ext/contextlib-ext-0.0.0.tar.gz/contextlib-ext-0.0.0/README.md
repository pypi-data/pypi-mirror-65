# contextlib-ext - extensions for contextlib

[![Build Status](https://cloud.drone.io/api/badges/nikicat/contextlib-ext/status.svg)](https://cloud.drone.io/nikicat/contextlib-ext)

`contextlib-ext` is a complimentary library for `contextlib`, it provides a following helpers:

## `suppress` as a decorator
`suppress` can be used as a decorator

```python
from contextlib_ext import suppress

@suppress(Exception)
def phony_func():
    raise ValueError

phony_func()
print("No exceptions")
```

## `@asynccontextmanager` creates decorator
`@asynccontextmanager` creates context manager that can be used as a decorator (`contextlib.contextmanager` already supports it)

```python
from contextlib_ext import asynccontextmanager

@asynccontextmanager
async def mymanager():
    yield

# The same as contextlib.asynccontextmanager
async with mymanager():
    pass

# This also works
@mymanager
async def myfunc():
    pass
```

## `async_suppress`
`async_suppress` - the same as `suppress`, but async

```python
from contextlib_ext import async_suppress

try:
  async with async_suppress(Exception):
      raise ValueError
except Exception:
  assert False  # never happens
else:
  print("No exceptions")

# Works as decorator too

@async_suppress(Exception)
async def phony_func():
    raise ValueError

phony_func()
print("No exceptions")
```
