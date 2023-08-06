# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import toml

from ..abc import *
from ..core import register_format

@register_format('toml', '.toml')
class TomlSerializer(ISerializer):
    format_name = 'toml'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return toml.loads(s, **kwargs)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return toml.dumps(obj, **kwargs)
