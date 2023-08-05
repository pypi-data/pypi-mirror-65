# -*- coding: utf-8 -*-

import logging

from spaceone.core.manager import BaseManager

__all__ = ['PluginRefManager']

_LOGGER = logging.getLogger(__name__)


class PluginRefManager(BaseManager):

    def __init__(self, transaction):
        super().__init__(transaction)
        self._installed_pluginref_model = self.locator.get_model('InstalledPluginRef')
        self._installed_plugin_model = self.locator.get_model('InstalledPlugin')
        #self._domain_id = self.transaction.meta['domain_id']

    def create(self, params):
        """ 
        Args:
            params:
              - domain_id: my domain_id
              - plugin_id
              - version
              - supervisor_ref
        """
        def _rollback(vo):
            vo.delete()

        if 'supervisor_id' not in params:
            supervisor = params['supervisor']
            params['supervisor_id'] = supervisor.supervisor_id
        _LOGGER.debug(f'[create] params: {params}')
        plugin_ref = self._installed_pluginref_model.create(params)

        self.transaction.add_rollback(_rollback, plugin_ref)
        return plugin_ref

    def get(self, supervisor_id, domain_id, plugin_id, version):
        """ Based on installed_plugin_ref, get real installed_plugin
        """
        params = {
            'supervisor_id': supervisor_id,
            'domain_id': domain_id,
            'plugin_id': plugin_id,
            'version': version
            }
        plugin_ref = self._installed_pluginref_model.get(supervisor_id = supervisor_id,
                                                        domain_id = domain_id,
                                                        plugin_id = plugin_id,
                                                        version = version)
        parent_domain_id = plugin_ref.supervisor.supervisor.domain_id
        plugin = self._installed_plugin_model.get(supervisor_id = supervisor_id,
                                                        domain_id = parent_domain_id,
                                                        plugin_id = plugin_id,
                                                        version = version)

        return plugin

    def delete(self, supervisor_id, domain_id, plugin_id, version):
        _LOGGER.debug(f'[delete] supervisor_id: {supervisor_id} at {domain_id}')
        plugin_ref = self.get(supervisor_id, domain_id, plugin_id, version)
        if plugin_ref:
            plugin_ref.delete()


def _query_domain_id(domain_id):
    return {
        'filter': [
            {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            }
        ]
    }
