# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail.com
# Created: 2019/11/23 09:21

import collections


def is_yes(value):
    return str(value).lower() in ('true', 'yes', 'si', 'y', 's', '1')


def tbiter(traceback):
    while traceback:
        yield traceback
        traceback = traceback.tb_next


def tblast(traceback):
    return [x for x in tbiter(traceback)][-1]


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
