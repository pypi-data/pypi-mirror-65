# -*- coding: utf-8 -*-

from spaceone.core.error import ERROR_BASE


class ERROR_REPOSITORY_BACKEND(ERROR_BASE):
    _status_code = 'INTERNAL'
    _message = 'Repository backend has problem. ({host})'


class ERROR_SUPERVISOR_STATE(ERROR_BASE):
    _status_code = 'USER_FAILURE?'
    _message = 'This "{action}" cannot be processed. (supervisor_id = {supervisor_id}, state = {state})'


class ERROR_SUPERVISOR_UPDATE(ERROR_BASE):
    _status_code = 'USER_FAILURE?'
    _message = 'This field is not updatable over "update" api. (key = {key})'


class ERROR_PLUGIN_STATE_CHANGE(ERROR_BASE):
    _status_code = 'USER_FAILURE?'
    _message = 'This "{action}" cannot be processed. (plugin_id = {supervisor_id}, state = {state})'
