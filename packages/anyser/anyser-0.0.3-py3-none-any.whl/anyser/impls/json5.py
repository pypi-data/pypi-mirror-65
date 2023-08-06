# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json5

from ..abc import *
from ..core import register_format

@register_format('json5', '.json5')
class Json5Serializer(ISerializer):
    format_name = 'json5'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return json5.loads(s, **kwargs)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {
            'ensure_ascii': Options.pop_ensure_ascii(options),
            'indent': Options.pop_indent(options),
        }
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return json5.dumps(obj, **kwargs)
