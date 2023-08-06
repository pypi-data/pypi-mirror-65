# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import pickle

from ..err import SerializeError
from ..abc import *
from ..err import NotSupportError
from ..core import register_format

@register_format('pickle')
class PickleSerializer(ISerializer):
    format_name = 'pickle'

    def loads(self, *_):
        raise NotSupportError('data format (pickle) does not support load from str.')

    def dumps(self, *_):
        raise NotSupportError('data format (pickle) does not support dump to str.')

    def loadb(self, s: bytes, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return pickle.loads(s, **kwargs)
        except pickle.UnpicklingError as e:
            raise SerializeError(e)

    def dumpb(self, obj, options: dict) -> bytes:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return pickle.dumps(obj, **kwargs)
        except pickle.PicklingError as e:
            raise SerializeError(e)
