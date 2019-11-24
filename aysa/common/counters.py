# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail.com
# Created: 2019/11/23 08:53

import time
from dotted.collection import DottedDict


class Counter:
    def __init__(self, name, factor=1, reset=0, tmpl=None, **kwargs):
        self.__name = name
        self._counter = None
        self._factor = factor
        self._reset = reset
        self._tmpl = tmpl or '{}="{}"'
        self.reset()

    @property
    def name(self):
        return self.__name

    @property
    def raw(self):
        raise NotImplementedError()

    def reset(self):
        self._counter = self._reset

    def sample(self, *args, **kwargs):
        raise NotImplementedError()

    def sampler(self):
        last_sample = [self.raw]

        def func():
            old_sample = last_sample[0]
            last_sample[0] = self.raw
            return self.sample(old_sample)

        return func

    def __str__(self):
        return self._tmpl.format(self.__name, self.raw)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.__str__())


class TotalCounter(Counter):
    @property
    def raw(self):
        return self._counter

    def increment(self):
        self._counter += self._factor

    def decrement(self):
        self._counter -= self._factor

    def sample(self, *args):
        return self.raw


class DeltaCounter(TotalCounter):
    def sample(self, other):
        return other - self.raw


class AverageCounter(Counter):
    def __init__(self, name, **kwargs):
        self._base_counter = None
        super().__init__(name, **kwargs)

    @property
    def raw(self):
        return self._counter, self._base_counter

    def reset(self):
        self._base_counter = self._reset
        super().reset()

    def add(self, value):
        self._counter += value
        self._base_counter += self._factor

    def sample(self, other):
        diff = other[1] - self.raw[1]
        if diff == 0:
            return 0
        return (other[0] - self.raw[0]) / diff


class RateCounter(TotalCounter):
    def __init__(self, name, func=None, **kwargs):
        self._func = func or time.time
        super().__init__(name, **kwargs)

    @property
    def raw(self):
        return self._counter, self._func()

    def sample(self, other):
        diff = other[1] - self.raw[1]
        if diff == 0:
            return 0
        return (other[0] - self.raw[0]) * self._factor / diff


class CounterManager(DottedDict):
    def register(self, counter):
        name = counter.name
        if not name.strip():
            raise ValueError('No se puede registrar un contador con el '
                             'nombre en blanco.')
        existing = self.get(name, None)
        if existing:
            if isinstance(existing, DottedDict):
                raise KeyError('No puede registrar un contador con el '
                               'nombre "%s" ya que el nombre de espacio '
                               'se encuentra registrado.' % existing)
            else:
                raise KeyError('No puede registrar un contador con el '
                               'nombre "%s" ya que el nombre del contador '
                               'se encuentra registrado.' % existing)
        try:
            self[name] = counter
            return counter
        except KeyError:
            raise KeyError('No puede registrar un contador con el nombre "%s" '
                           'ya que una parte de este nombre de espacio ya se '
                           'encuentra registrado.' % name)


global_manager = CounterManager()


def total_counter(name, manager=global_manager, **kwargs):
    return manager.register(TotalCounter(name, **kwargs))


def delta_counter(name, manager=global_manager, **kwargs):
    return manager.register(DeltaCounter(name, **kwargs))


def average_counter(name, manager=global_manager, **kwargs):
    return manager.register(AverageCounter(name, **kwargs))


def rate_counter(name, factor=1, manager=global_manager, **kwargs):
    return manager.register(RateCounter(name, factor=factor, **kwargs))


class Meter:
    def __init__(self):
        self.__counters = {}

    def add(self, key, value):
        pass

    def sample(self):
        pass
