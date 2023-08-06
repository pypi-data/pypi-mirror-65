# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Optional, Any, Union
from contextlib import contextmanager
from io import IOBase

from .err import *
from .abc import *

_REGISTERED_SERIALIZERS = {}

def register_format(*keys):
    '''
    register a serializer class for load and dump.
    '''
    def decorator(cls):
        for k in keys:
            _REGISTERED_SERIALIZERS[k] = cls
        return cls
    return decorator


def get_available_formats() -> list:
    '''
    get all available formats.
    '''
    return list(_REGISTERED_SERIALIZERS)


def find_serializer(format: str) -> Optional[ISerializer]:
    if not isinstance(format, str):
        raise TypeError

    cls = _REGISTERED_SERIALIZERS.get(format)
    if cls is not None:
        return cls()


def _get_required_serializer(format: str) -> ISerializer:
    serializer = find_serializer(format)
    if not serializer:
        raise FormatNotFoundError(format)
    return serializer

def load(s: Union[str, bytes, IOBase], format: str, **options) -> Any:
    'load a obj from source.'
    if not isinstance(s, (str, bytes, IOBase)):
        raise TypeError
    serializer = _get_required_serializer(format)
    return serializer.load(s, options)

def loads(s: str, format: str, **options) -> Any:
    'load a obj from str.'
    if not isinstance(s, str):
        raise TypeError
    serializer = _get_required_serializer(format)
    return serializer.loads(s, options)

def loadb(b: bytes, format: str, **options) -> Any:
    'load a obj from bytes.'
    if not isinstance(b, bytes):
        raise TypeError
    serializer = _get_required_serializer(format)
    return serializer.loadb(b, options)

def loadf(fp: IOBase, format: str, **options) -> Any:
    'load a obj from a file-like object.'
    if not isinstance(fp, IOBase):
        raise TypeError
    serializer = _get_required_serializer(format)
    return serializer.loadf(fp, options)

def dumps(obj, format: str, **options) -> str:
    '''
    dump a obj to str.

    options:

    - `ensure_ascii` - `bool`, default `True`.
    - `indent` - `int?`, default `None`.
    - `origin_kwargs` - `dict`, pass to serializer
    '''
    serializer = _get_required_serializer(format)
    return serializer.dumps(obj, options)

def dumpb(obj, format: str, **options) -> bytes:
    '''
    dump a obj to bytes.

    options:

    - `encoding` - `str`, default `utf-8`.
    - `ensure_ascii` - `bool`, default `True`.
    - `indent` - `int?`, default `None`.
    - `origin_kwargs` - `dict`, pass to serializer
    '''
    serializer = _get_required_serializer(format)
    return serializer.dumpb(obj, options)

def dumpf(obj, fp: IOBase, format: str, **options):
    '''
    dump a obj into the file-like object.

    options:

    - `encoding` - `str`, default `utf-8`.
    - `ensure_ascii` - `bool`, default `True`.
    - `indent` - `int?`, default `None`.
    - `origin_kwargs` - `dict`, pass to serializer
    '''
    if not isinstance(fp, IOBase):
        raise TypeError
    serializer = _get_required_serializer(format)
    return serializer.dumpf(obj, fp, options)
