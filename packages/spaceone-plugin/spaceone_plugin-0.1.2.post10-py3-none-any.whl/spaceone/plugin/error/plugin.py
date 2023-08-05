# -*- coding: utf-8 -*-
from spaceone.core.error import *


class ERROR_PLUGIN_NOT_FOUND(ERROR_BASE):
    _message = 'plugin_id does not exist. {plugin_id}'

