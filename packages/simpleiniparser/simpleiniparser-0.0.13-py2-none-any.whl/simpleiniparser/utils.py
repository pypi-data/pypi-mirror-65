from functools import wraps

try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec


def from_self(function):
    """
    >>> class DummyTestCase:
    ...     def __init__(self):
    ...         self.setinsetup = 2
    ...     @from_self
    ...     def test_something(self, setinsetup):
    ...         return setinsetup
    ...
    >>> dummytest = DummyTestCase()
    >>> dummytest.test_something()
    2
    """
    names = getfullargspec(function).args[1:]

    @wraps(function)
    def fetch_and_call(self, *args, **kwargs):
        kwargs = {name: getattr(self, name) for name in names}
        return function(self, *args, **kwargs)

    return fetch_and_call
