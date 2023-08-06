from contextlib import ContextDecorator, _AsyncGeneratorContextManager, suppress as orig_suppress
from functools import wraps


class suppress(orig_suppress, ContextDecorator):
    pass


class AsyncGeneratorContextManager(_AsyncGeneratorContextManager):
    def _recreate_cm(self):
        return self.__class__(self.func, self.args, self.kwds)

    def __call__(self, func):
        @wraps(func)
        async def inner(*args, **kwds):
            async with self._recreate_cm():
                return await func(*args, **kwds)
        return inner


def asynccontextmanager(func):
    @wraps(func)
    def helper(*args, **kwds):
        return AsyncGeneratorContextManager(func, args, kwds)
    return helper


@asynccontextmanager
async def async_suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass
