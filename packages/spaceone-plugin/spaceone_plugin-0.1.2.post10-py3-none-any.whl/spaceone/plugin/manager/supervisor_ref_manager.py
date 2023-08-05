# -*- coding: utf-8 -*-

import logging

from spaceone.core.manager import BaseManager

__all__ = ['SupervisorRefManager']

_LOGGER = logging.getLogger(__name__)

class SupervisorRefManager(BaseManager):

    def __init__(self, transaction):
        super().__init__(transaction)
        self._supervisor_ref_model = self.locator.get_model('SupervisorRef')

    def create(self, params):
        """ 
        Args:
            params:
              - supervisor_id: parent supervisor_id
              - domain_id: my domain_id
        """
        def _rollback(vo):
            vo.delete()

        _LOGGER.debug(f'[create] params: {params}')
        supvr_ref = self._supervisor_ref_model.create(params)

        self.transaction.add_rollback(_rollback, supvr_ref)
        return supvr_ref

    def get(self, supervisor_id, domain_id):
        return self._supervisor_ref_model.get(supervisor_id=supervisor_id, domain_id=domain_id)

    def delete(self, supervisor_id, domain_id):
        _LOGGER.debug(f'[delete] supervisor_id: {supervisor_id} at {domain_id}')
        supvr_ref = self.get(supervisor_id, domain_id)
        if supvr_ref:
            supvr_ref.delete()

    def list_supervisor(self, query):
        return self._supervisor_ref_model.query(**query)


    def update(self, params):
        supvr_ref = self._get_supvr_ref_by_ref_id(params['reference_id'])
        # TODO: rollback
        return supvr_ref.update(params)


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
