# -*- coding: utf-8 -*-

import logging
import time

from spaceone.core.error import ERROR_NOT_FOUND
from spaceone.core.manager import BaseManager
from spaceone.plugin.manager.plugin_manager.plugin_state import PluginStateMachine, ACTIVE, PROVISIONING, \
    RE_PROVISIONING
from spaceone.plugin.model import *

__all__ = ['PluginManager']

_LOGGER = logging.getLogger(__name__)

WAIT_TIMEOUT = 60

class PluginManager(BaseManager):
    def __init__(self, transaction):
        super().__init__(transaction)
        self._installed_plugin_model: InstalledPlugin = self.locator.get_model('InstalledPlugin')

        if 'domain_id' in self.transaction.meta:
            self.domain_id = self.transaction.meta['domain_id']
        else:
            self.domain_id = None
            _LOGGER.info("[__init__] domain_id is not determined")

    def _update_domain_id(self):
        if self.domain_id == None:
            if 'domain_id' in self.transaction.meta:
                self.domain_id = self.transaction.meta['domain_id']
            else:
                _LOGGER.error(f'[_update_domain_id] domain_id does not exist in transaction.meta:{self.transaction.meta}')

    def create(self, params):
        """ 
        Args:
            params(dict) : {
                    'domain_id' : str,
                    'plugin_id' : str,
                    'version'   : str,
                    'supervisor': str
                }
        """
        def _rollback(vo):
            vo.delete()

        if 'supervisor_id' not in params:
            supervisor = params['supervisor']
            params['supervisor_id'] = supervisor.supervisor_id
        _LOGGER.debug(f'[create] params: {params}')

        plugin = self._installed_plugin_model.create(params)
        self.transaction.add_rollback(_rollback, plugin)

        # Check plugin_id exist or not
        repo_connector = self.locator.get_connector('RepositoryConnector')
        repo_connector.get_plugin(params['plugin_id'], params['domain_id'])

        return plugin

    def get(self, supervisor_id, domain_id, plugin_id, version):
        """ get installed_plugin
        """
        plugin = self._installed_plugin_model.get(supervisor_id=supervisor_id,
                                                domain_id=domain_id,
                                                plugin_id=plugin_id,
                                                version=version)
        return plugin

    def exist(self, supervisor_id, domain_id, plugin_id, version):
        """ exist installed_plugin
        """
        try:
            plugin = self._installed_plugin_model.get(supervisor_id=supervisor_id,
                                                    domain_id=domain_id,
                                                    plugin_id=plugin_id,
                                                    version=version)
            return (True, plugin)
        except:
            return (False, None)


    def _get_installed_plugin(self, plugin_id, version):
        return self._installed_plugin_model.get(plugin_id=plugin_id, version=version)

    def install_plugin(self, params):
        def _rollback(vo):
            vo.delete()

        plugin_vo: InstalledPlugin = self._installed_plugin_model.create(params)
        self.transaction.add_rollback(_rollback, plugin_vo)

        return plugin_vo

    def update_plugin(self, params):
        def _rollback(old_data: dict):
            plugin_vo.update(old_data)

        plugin_vo: InstalledPlugin = self._get_installed_plugin(params['plugin_id'], params['version'])
        self.transaction.add_rollback(_rollback, plugin_vo.to_dict())

        return plugin_vo.update(params)

    def activate_plugin(self, params):
        def _rollback(old_data: dict):
            plugin_vo.update(old_data)

        plugin_vo: InstalledPlugin = self._get_installed_plugin(plugin_id=params['plugin_id'], version=params['version'])
        self.transaction.add_rollback(_rollback, plugin_vo.to_dict())

        plugin_state_machine = PluginStateMachine(params['plugin_id'], plugin_vo.state)
        state = plugin_state_machine.activate()
        params['state'] = state

        return plugin_vo.update(params)

    def update_plugin_state(self, plugin_id, version, state, endpoint, supervisor_id):
        plugin_vo = self._installed_plugin_model.get(supervisor_id=supervisor_id, 
                                            plugin_id=plugin_id, 
                                            version=version)
        return plugin_vo.update({'state':state, 'endpoint':endpoint})

    def make_reprovision(self, plugin_id, version):
        def _rollback(old_data: dict):
            plugin_vo.update(old_data)

        plugin_vo: InstalledPlugin = self._get_installed_plugin(plugin_id=plugin_id, version=version)
        self.transaction.add_rollback(_rollback, plugin_vo.to_dict())

        plugin_state_machine = PluginStateMachine(plugin_id, plugin_vo.state)
        state = plugin_state_machine.make_reprovision()

        return plugin_vo.update({'state': state})

    def mark_failure(self, plugin_id, supervisor_id, version):
        def _rollback(old_data: dict):
            plugin_vo.update(old_data)

        plugin_vo: InstalledPlugin = self._installed_plugin_model.get(
            plugin_id=plugin_id,
            version=version,
            supervisor_id=supervisor_id
        )
        if plugin_vo.supervisor.supervisor_id != supervisor_id:
            raise ERROR_NOT_FOUND(key='supervisor.supervisor_id', value=supervisor_id)

        self.transaction.add_rollback(_rollback, plugin_vo.to_dict())

        plugin_state_machine = PluginStateMachine(plugin_id, plugin_vo.state)
        state = plugin_state_machine.change_to_error()

        return plugin_vo.update({'state': state})

    def wait_until_activated(self, plugin_id, version, supervisor_id):
        count = 0
        while True:
            installed_plugin = self._safe_delay_get_installed_plugin(supervisor_id, plugin_id, version,  3)
            if installed_plugin and installed_plugin.state == ACTIVE:
                break
            # Wait
            count = count + 1
            if count > WAIT_TIMEOUT:
                _LOGGER.error("[wait_until_activated] Timeout for activate")
                # TODO: add Error class
                break
            time.sleep(1)
            
        return installed_plugin

    # Verify
    def get_secret_data(self, secret_id, domain_id):
        connector = self.locator.get_connector('SecretConnector')
        return connector.get_data(secret_id, domain_id)

    def call_verify_plugin(self, plugin_endpoint, options, secret_data):
        """ Call verify function at endpoint
        """
        # Issue: CLOUD-941

    def _safe_delay_get_installed_plugin(self, supervisor_id, plugin_id, version, delay_second=0):
        if 0 < delay_second < 30:
            time.sleep(delay_second)

        try:
            data = self._installed_plugin_model.get(supervisor_id=supervisor_id, plugin_id=plugin_id, version=version)
        except ERROR_NOT_FOUND:
            data = None
        return data



# Static method
def _make_plugin_params(supervisor, plugin_id, image, version, name):
    return {
        'supervisor': supervisor,
        'supervisor_id': supervisor.supervisor_id,
        'domain_id': supervisor.domain_id,
        'name': name,
        'plugin_id': plugin_id,
        'image': image,
        'version': version
    }
