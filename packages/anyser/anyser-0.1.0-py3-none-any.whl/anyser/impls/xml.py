# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import xml.etree.ElementTree as et

from ..err import SerializeError
from ..abc import *
from ..core import register_format

@register_format('xml', '.xml')
class XmlSerializer(ISerializer):
    format_name = 'xml'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return et.fromstring(s)
        except et.ParseError as e:
            raise SerializeError(e)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return et.tostring(obj, encoding='unicode', **kwargs)
        except AttributeError as e:
            raise SerializeError(e)

