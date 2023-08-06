# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

class FormatNotFoundError(Exception):
    pass

class SerializeError(Exception):
    'raise when serialize or deserialize from bad data.'
    pass

class NotSupportError(Exception):
    pass
