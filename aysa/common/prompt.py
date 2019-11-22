# Author: Alejandro M. BERNARDIS
# Email: alejandro.bernardis@gmail.com
# Created: 2019/11/22 15:34
# ~

from inspect import getdoc
from docopt import docopt, DocoptExit


def docstring(obj, tmpl=' \n{}\n \n'):
    if not isinstance(obj, str):
        obj = getdoc(obj)
    if tmpl is not None:
        return tmpl.format(obj)
    return obj


def _extras(help, version, options, doc):
    if help and any((o.name in ('-h', '--help')) and o.value for o in options):
        raise HelpCommand(doc)
    if version and any(o.name == '--version' and o.value for o in options):
        print(version)


def docoptions(obj, *args, **kwargs):
    obj = docstring(obj)
    try:
        docopt.extras = _extras
        return docopt(obj, *args, **kwargs), obj
    except DocoptExit:
        raise ValueError(obj)


class HelpCommand(Exception):
    def __init__(self, doc):
        super().__init__()
        self.doc = doc
