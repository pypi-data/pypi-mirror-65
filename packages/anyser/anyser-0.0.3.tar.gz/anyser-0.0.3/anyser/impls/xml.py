# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import xml.etree.ElementTree as et

from ..abc import *
from ..core import register_format

@register_format('xml', '.xml')
class XmlSerializer(ISerializer):
    format_name = 'xml'

    def loads(self, s: str, options: dict):
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return et.fromstring(s)

    def dumps(self, obj, options: dict) -> str:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        return et.tostring(obj, encoding='unicode', **kwargs)
