# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail.com
# Created: 2019/11/23 08:53


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
        return other.raw - self.raw


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
