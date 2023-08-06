# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import toml

from ..err import SerializeError
from ..abc import *
from ..core import register_format

@register_format('toml', '.toml')
class TomlSerializer(ISerializer):
    format_name = 'toml'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return toml.loads(s, **kwargs)
        except toml.decoder.TomlDecodeError as e:
            raise SerializeError(e)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return toml.dumps(obj, **kwargs)
        except TypeError as e:
            raise SerializeError(e)
