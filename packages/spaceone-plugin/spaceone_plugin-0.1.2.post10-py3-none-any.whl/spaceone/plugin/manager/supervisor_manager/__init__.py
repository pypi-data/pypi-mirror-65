# -*- coding: utf-8 -*-

import logging
import random

from spaceone.core.manager import BaseManager

from spaceone.plugin.error import *
from spaceone.plugin.manager.supervisor_manager.supervisor_state import SupvrStateMachine

__all__ = ['SupervisorManager']

_LOGGER = logging.getLogger(__name__)


class SupervisorManager(BaseManager):
    def __init__(self, transaction):
        super().__init__(transaction)
        self._supervisor_model = self.locator.get_model('Supervisor')
        self._installed_plugin_model = self.locator.get_model('InstalledPlugin')

        if 'domain_id' in self.transaction.meta:
            self.domain_id = self.transaction.meta['domain_id']
        else:
            self.domain_id = None
            _LOGGER.info('[__init__] domain_id is not determined')

    def _update_domain_id(self):
        if self.domain_id == None:
            if 'domain_id' in self.transaction.meta:
                self.domain_id = self.transaction.meta['domain_id']
            else:
                _LOGGER.error(f'[_update_domain_id] domain_id does not exist in transaction.meta:{self.transaction.meta}')


    def create(self, params):
        def _rollback(vo):
            vo.delete()

        self._update_domain_id()

        _LOGGER.debug(f'[create] params: {params}')
        supvr: Supervisor = self._supervisor_model.create(params)
        SupvrStateMachine(supvr.supervisor_id, supvr.state)

        # TODO: add rollback

        return supvr

    def get_by_hostname(self, hostname, domain_id):
        return self._supervisor_model.get(hostname=hostname, domain_id=domain_id)

    def get_by_id(self, supervisor_id, domain_id):
        return self._supervisor_model.get(supervisor_id=supervisor_id, domain_id=domain_id)

    def get_by_id_or_hostname(self, supervisor_id, hostname, domain_id):
        if supervisor_id and hostname:
            return self._supervisor_model.get(supervisor_id=supervisor_id, hostname=hostname, domain_id=domain_id)
        if supervisor_id:
            return self._supervisor_model.get(supervisor_id=supervisor_id, domain_id=domain_id)
        if hostname:
            return self._supervisor_model.get(hostname=hostname, domain_id=domain_id)
        raise ERROR_NO_POSSIBLE_SUPERVISOR(params=domain_id) 

    def delete(self, supervisor_id, domain_id):
        supvr = self.get_by_id(supervisor_id, domain_id)
        supvr.delete()
        # TODO: add rollback

    def register(self, supervisor_id, domain_id):
        # TODO: add rollback
        supvr: Supervisor = self.get_by_id(supervisor_id, domain_id)

        _LOGGER.debug(f'supvr: {supvr.to_dict()}')

        supvr_state_machine = SupvrStateMachine(supervisor_id, supvr.state)
        supvr_state_machine.register()

        return supvr.update({'state': str(supvr_state_machine.state)})

    def update(self, params):
        """
        Update method updates only [is_public, priority, labels, tags] fields.
        :param params: Supervisor
        :return: Supervisor
        """
        self._update_domain_id()

        supvr: Supervisor = self._supervisor_model.get(
            supervisor_id=params['supervisor_id'],
            domain_id=params['domain_id']
        )

        updatable_fields = ['is_public', 'priority', 'labels', 'tags', 'supervisor_id', 'domain_id']
        for key in list(params.keys()):
            if key not in updatable_fields:
                raise ERROR_SUPERVISOR_UPDATE(key=key)
        # TODO: add rollback
        return supvr.update(params)

    def enable(self, supervisor_id, domain_id):
        supvr: Supervisor = self.get_by_id(supervisor_id, domain_id)

        supvr_state_machine = SupvrStateMachine(supervisor_id, supvr.state)
        supvr_state_machine.enable()
        # TODO: add rollback
        return supvr.update({'state': str(supvr_state_machine.state)})

    def disable(self, supervisor_id, domain_id):
        supvr: Supervisor = self.get_by_id(supervisor_id, domain_id)

        supvr_state_machine = SupvrStateMachine(supervisor_id, supvr.state)
        supvr_state_machine.disable()
        # TODO: add rollback
        return supvr.update({'state': str(supvr_state_machine.state)})

    def get_all_supervisors(self, domain_id):
        return self.list_supervisors(_query_domain_id(domain_id))

    def list_supervisors(self, query):
        return self._supervisor_model.query(**query)

    def get_matched_supervisor(self, domain_id, labels):
        supervisors, total_count = self.get_all_supervisors(domain_id)
        matched_supvr = _get_matched_supervisor(supervisors, labels)
        _LOGGER.debug(f'[get_matched_supervisor] matched_supvr: {matched_supvr}')
        return matched_supvr

    def get_public_supervisor(self, labels):
        query = _query_public()
        supervisors, total_count = self.list_supervisors(query)
        _LOGGER.debug(f'[get_public_supervisor] {total_count}')

        matched_supvr = _get_matched_supervisor(supervisors, labels)
        return matched_supvr

    def list_plugins(self, query):
        _LOGGER.debug(f'[supervisor_manager] list_plugins: {query}')
        return self._installed_plugin_model.query(**query)


def _get_matched_supervisor(supervisors, labels):
    matched_supervisors = list(map(
        lambda supvr: supvr if set(supvr.labels).issuperset(labels) else None,
        supervisors
    ))

    if matched_supervisors and len(matched_supervisors) > 0:
        return random.choice(matched_supervisors)
    return None


def _query_domain_id_and_enabled(domain_id):
    return {
        'filter': [
            {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            },
            {
                'k': 'state',
                'v': 'ENABLED',
                'o': 'eq'
            }
        ]
    }


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


def _query_domain_id_or_public(domain_id):
    return {
        'filter_or': [
            {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            },
            {
                'k': 'is_public',
                'v': True,
                'o': 'eq'
            }
        ],
        'filter': [
            {
                'k': 'state',
                'v': 'ENABLED',
                'o': 'eq'
            }
        ]
    }

def _query_public():
    return {
        'filter': [
            {
                'k': 'is_public',
                'v': True,
                'o': 'eq'
            },
            {
                'k': 'state',
                'v': 'ENABLED',
                'o': 'eq'
            }
        ]
    }


# def _domain_params():
#     return {
#         'name': name,
#         'hostname': hostname,
#         'secret_key': secret_key,
#         'plugin_info': plugin_info,
#         'tags': tags
#     }
