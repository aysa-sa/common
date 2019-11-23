# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail.com
# Created: 2019/11/23 08:53


class Counter:
    def __init__(self, name, factor=1, reset=0, tmpl=None):
        self.__name = name
        self._counter = None
        self._factor = factor
        self._reset = reset
        self._tmpl = tmpl or '{}: {}'
        self.reset()

    @property
    def name(self):
        return self.__name

    def reset(self):
        self._counter = self._reset

    @property
    def total(self):
        return self._counter

    def increment(self, *args, **kwargs):
        raise NotImplementedError()

    def decrement(self, *args, **kwargs):
        raise NotImplementedError()

    def __str__(self):
        return self._tmpl.format(self.__name, self.total)

    def __repr__(self):
        return self.__str__()


class TotalCounter(Counter):
    def increment(self):
        self._counter += self._factor

    def decrement(self):
        self._counter -= self._factor
