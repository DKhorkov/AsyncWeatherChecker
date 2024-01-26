import inspect
import asyncio

from typing import Callable, Tuple, Dict, Type, LiteralString


def _async_wrapper(old_class_method: Callable) -> Callable:
    """
    Decorator for testing asynchronous methods

    https://stackoverflow.com/questions/70015634/how-to-test-async-function-using-pytest
    :param old_class_method: Function, that should be run asynchronous
    """

    def wrapper(*args, **kwargs):
        return asyncio.run(old_class_method(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(old_class_method)  # without this, PyTest fixtures are not injected
    return wrapper


class AsyncMetaclass(type):
    """
    Metaclass for implementing Adapter pattern for decorating all class methods purpose.
    """

    def __new__(cls, name: LiteralString, bases: Tuple[Type], cls_attrs: Dict):
        """
        Processes overridable class attributes and methods.
        If not static method, it will be decorated with _async_wrapper.
        After processing all methods, new class will be returned.

        :param name: Class name
        :param bases: Parents, from which class was inherited
        :param cls_attrs: Class attributes and methods
        """
        new_cls_attrs = dict()
        for attr_name, attr_value in cls_attrs.items():
            if callable(attr_value) and not isinstance(attr_value, staticmethod):
                new_cls_attrs[attr_name] = _async_wrapper(attr_value)
            else:
                new_cls_attrs[attr_name] = attr_value

        return super().__new__(cls, name, bases, new_cls_attrs)
