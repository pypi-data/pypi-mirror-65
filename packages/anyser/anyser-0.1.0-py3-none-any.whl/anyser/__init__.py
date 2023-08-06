# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import importlib

from .err import FormatNotFoundError, SerializeError, NotSupportError
from .abc import ISerializer
from .core import (
    load,
    loads, loadb, loadf,
    dumps, dumpb, dumpf,
    register_format, get_available_formats,
)

def _import_impls():
    impls_root = os.path.join(os.path.dirname(__file__), 'impls')
    for name in os.listdir(impls_root):
        if name.endswith('.py') and not name.startswith('_'):
            try:
                importlib.import_module('.impls.' + name[:-3], __name__)
            except ModuleNotFoundError:
                pass

_import_impls()

__all__ = (
    'FormatNotFoundError', 'SerializeError', 'NotSupportError',
    'ISerializer',
    'load',
    'loads', 'dumps', 'loadf',
    'loadb', 'dumpb', 'dumpf',
    'register_format', 'get_available_formats',
)
