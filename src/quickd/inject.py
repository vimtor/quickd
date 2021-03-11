from inspect import ismethod
from typing import get_type_hints

from .singletons import constructors, instances


def is_method(obj: object, func):
    name = func.__name__
    return hasattr(obj, name) and ismethod(getattr(obj, name))


def inject(function):
    hints = get_type_hints(function)
    default_args = []

    def wrapper(*args):
        if not default_args:
            for arg_name, arg_type in hints.items():
                if arg_name == 'return':
                    continue
                elif arg_type in instances:
                    default_args.append(instances[arg_type])
                elif arg_type in constructors:
                    instance = constructors[arg_type]()
                    instances[arg_type] = instance
                    default_args.append(instance)
                else:
                    raise KeyError("You forgot to define an instance for " + arg_type.__name__)
        final_args = default_args
        if len(args) > 0:
            if is_method(args[0], function):
                final_args = (*args, *default_args)[:len(hints) + 1]
            else:
                final_args = args
        return function(*final_args)

    return wrapper
