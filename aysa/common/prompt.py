# Author: Alejandro M. BERNARDIS
# Email: alejandro.bernardis@gmail.com
# Created: 2019/11/22 15:34
# ~

import sys
import json
from inspect import getdoc
from docopt import docopt
from functools import partialmethod


def is_writable(output):
    if not all([hasattr(output, 'write'), hasattr(output, 'flush')]):
        raise TypeError('El objeto "%s" no posee los métodos '
                        '"write" y/o "flush".' % output)


class WritableObject:
    def __init__(self, output, parser=None):
        is_writable(output)
        self.__output = output
        self.__parser = parser

    def parse(self, *args, **kwargs):
        if self.__parser is None:
            raise NotImplementedError()
        return self.__parser(*args, **kwargs)

    def write(self, *args, **kwargs):
        value = self.parse(*args, **kwargs)
        if value is not None:
            self.__output.write(value)

    def flush(self):
        self.__output.flush()


class StdOut(WritableObject):
    def __init__(self, parser=None):
        super().__init__(sys.__stdout__, parser)
        self._ = sys.stdout
        sys.stdout = self


class StdErr(WritableObject):
    def __init__(self, parser=None):
        super().__init__(sys.__stderr__, parser)
        self._ = sys.stderr
        sys.stderr = self


class Printer:
    def __init__(self, output=sys.stdout):
        is_writable(output)
        self.__output = output

    def _parse(self, *message, sep=' ', end='\n', endx=None, tab=0, tmpl=None,
               prefix='', subffix='', **kwargs):
        message = tmpl.format(*message) if tmpl is not None \
            else sep.join([str(x) for x in message])
        message = prefix + message + subffix
        if endx is not None:
            end = (end or '\n') * max(1, endx or 1)
        if end and not message.endswith(end):
            message += end
        for x in ('lower', 'upper', 'title', 'capitalize', 'swapcase'):
            if kwargs.get(x, False) is True:
                message = getattr(message, x)()
                break
        return (' ' * tab) + message

    def write(self, *message, **kwargs):
        value = self._parse(*message, **kwargs)
        value and self.__output.write(value)

    def flush(self, *message, **kwargs):
        if message:
            self.write(*message, **kwargs)
        self.__output.flush()

    def done(self):
        self.flush('Done')

    def blank(self):
        self.flush('')

    def rule(self, size=1, char='-'):
        self.flush(char * max(1, size or 1))

    def header(self, *message, **kwargs):
        self.blank()
        self.write(*message, **kwargs)
        self.rule(2)

    def footer(self, *message, **kwargs):
        self.blank()
        self.rule(2)
        self.write(*message, **kwargs)
        self.blank()

    def json(self, value, indent=2):
        raw = json.dumps(value, indent=indent, default=str) \
            if isinstance(value, dict) else '-'
        self.__output.write(raw + '\n')
        self.flush()

    error = partialmethod(write, subffix='!')
    question = partialmethod(write, subffix='?')
    bullet = partialmethod(write, prefix='> ')

    def __call__(self, *args, **kwargs):
        self.flush(*args, **kwargs)


def raw_input(self, message=None, recursive=False, default=None, values=None,
              cast=None):
    if not isinstance(message, str):
        message = 'Por favor, ingrese un valor'
    else:
        message = message.strip()
    if not message.endswith(':'):
        message += ': '
    if values or default:
        if not values:
            values = default
        message = '{} [{}]: '.format(message[:-2], str(values))
    value = input(message).strip()
    if default is not None and not value:
        return default
    if cast is not None:
        try:
            value = cast(value)
        except Exception:
            if recursive is True:
                return self.input(message, recursive, default, cast)
            raise TypeError('Valor incorrecto: ' + value)
    return value


def docstring(obj, tmpl=' \n{}\n \n'):
    if not isinstance(obj, str):
        obj = getdoc(obj)
    if tmpl is not None:
        return tmpl.format(obj)
    return obj


def docoptions(obj, *args, **kwargs):
    obj = docstring(obj)
    return docopt(obj, *args, **kwargs), obj
