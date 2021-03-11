from typing import get_type_hints

from .singletons import instances


def factory(function):
    hints = get_type_hints(function)
    return_type = hints['return']
    if not return_type:
        raise ValueError('Function decorated with @factory must have a return type annotation')
    instances[return_type] = function()
