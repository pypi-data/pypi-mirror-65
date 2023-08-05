# -*- coding: utf-8 -*-
from spaceone.core.error import *


class ERROR_NO_POSSIBLE_SUPERVISOR(ERROR_BASE):
    _message = 'There is no supervisor to run plugin. params: {params}'

class ERROR_NOT_SUPPORT_RECOVER_PLUGIN(ERROR_BASE):
    _message = 'recover_plugin is not supported. supervisor_id: {supervisor_id}'

class ERROR_NOT_SUPPORT_LIST_PLUGINS(ERROR_BASE):
    _message = 'This supervisor does not support list plugins: {supervisor_id}'
