# Copyright (c) 2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""A really easy way to use argparse."""

import argparse
import collections.abc
import inspect
import sys


def error(msg):
    """Print an error message to stderr and exit with status 2."""
    print("%s: error: %s" % (sys.argv[0], msg), file=sys.stderr)
    print("Run '%s --help' for more info." % sys.argv[0], file=sys.stderr)
    sys.exit(2)


class _ArgParser(argparse.ArgumentParser):

    def __init__(self, docstring, **kwargs):
        self.__doc = inspect.cleandoc(docstring)
        super().__init__(**kwargs)

    def format_help(self):
        return self.format_usage() + '\n' + self.__doc + '\n'

    def error(self, msg):
        error(msg)


def _set_action_or_type(cls, kwargs):
    if issubclass(cls, bool):
        kwargs['action'] = 'store_true'
    else:
        kwargs['type'] = cls


def program(func):
    """Return a function that parses arguments based on func's signature.

    Use this as a decorator.
    """
    if func.__doc__ is None:
        raise ValueError("the function must have a docstring")

    add_argument_args = []

    signature = inspect.signature(func)
    for underscorename, param in signature.parameters.items():
        dashname = underscorename.replace('_', '-')
        args = []
        kwargs = {}

        # set up action, type or choices
        if param.annotation is inspect.Parameter.empty:
            # try to guess from default, if any
            if param.default is not inspect.Parameter.empty:
                if isinstance(param.default, bool) and param.default:
                    raise ValueError("False is not a valid default value")
                _set_action_or_type(type(param.default), kwargs)
        else:
            # use the annotation
            if isinstance(param.annotation, collections.abc.Sequence):
                # allow a sequence of possible values as an annotation
                if not param.annotation:
                    raise ValueError("no possible %r values were given"
                                     % underscorename)
                kwargs['choices'] = param.annotation
                kwargs['type'] = type(param.annotation[0])
            else:
                _set_action_or_type(param.annotation)

        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append('--' + dashname)
            if param.default is inspect.Parameter.empty:
                # def thing(*, foo): ...
                kwargs['required'] = True
            else:
                # def thing(*, foo=default): ...
                kwargs['default'] = param.default

        elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            args.append(dashname)
            if param.default is inspect.Parameter.empty:
                # def thing(foo): ...
                pass
            else:
                # def thing(foo=default): ...
                kwargs['nargs'] = argparse.OPTIONAL
                kwargs['default'] = param.default

        else:
            raise ValueError("unknown parameter kind %r" % param.kind)
        add_argument_args.append((args, kwargs))

    def main():
        parser = _ArgParser(func.__doc__)
        for args, kwargs in add_argument_args:
            parser.add_argument(*args, **kwargs)
        return func(**parser.parse_args().__dict__)

    return main
