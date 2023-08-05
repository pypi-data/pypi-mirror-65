# -*- coding: utf-8 -*-
import functools

from spaceone.api.plugin.v1 import plugin_pb2
from spaceone.api.plugin.v1 import supervisor_pb2

from spaceone.core.pygrpc.message_type import *

__all__ = ['PluginInfo', 'PluginsInfo', 'PluginEndpoint']


def PluginInfo(plugin_vo):
    info = {}
    info['plugin_id'] = plugin_vo.plugin_id
    info['version'] = plugin_vo.version
    info['state'] = plugin_vo.state
    info['endpoint'] = plugin_vo.endpoint

    return supervisor_pb2.PluginInfo(**info)


def PluginsInfo(plugin_vo, total_count):
    results = list(map(functools.partial(PluginInfo), plugin_vo))

    return supervisor_pb2.PluginsInfo(results=results, total_count=total_count)

def PluginEndpoint(plugin_vo):
    info = {}
    info['endpoint'] = plugin_vo.endpoint

    return plugin_pb2.PluginEndpoint(**info)
