# Author: Alejandro M. BERNARDIS
# Email: alejandro.bernardis@gmail.com
# Created: 2019/11/22 15:31
# ~

import sys
import json
from functools import partialmethod


class Printer:
    def __init__(self, output=sys.stdout):
        if not all([hasattr(output, 'write'), hasattr(output, 'flush')]):
            raise TypeError('El objeto "%s" no posee los métodos '
                            '"write" y/o "flush".' % output)
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