import inspect
import asyncio

from typing import Callable


def _async_wrapper(old_class_method: Callable) -> Callable:
    """
    https://stackoverflow.com/questions/70015634/how-to-test-async-function-using-pytest
    :param async_func: Function, that should be run asynchronous
    """

    def wrapper(*args, **kwargs):
        return asyncio.run(old_class_method(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(old_class_method)  # without this, PyTest fixtures are not injected
    return wrapper


class AsyncMetaclass(type):
    """
    Metaclass for implementing Adapter pattern for decorating all class methods purpose.
    """

    def __new__(cls, name, parents, cls_attrs):
        new_cls_attrs = dict()
        for attr_name, attr_value in cls_attrs.items():
            if callable(attr_value) and not isinstance(attr_value, staticmethod):
                new_cls_attrs[attr_name] = _async_wrapper(attr_value)
            else:
                new_cls_attrs[attr_name] = attr_value

        return super().__new__(cls, name, parents, new_cls_attrs)