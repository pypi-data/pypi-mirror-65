# -*- coding: utf-8 -*-

import logging

from spaceone.core.error import *
from spaceone.core.service import *
from spaceone.plugin.model import Supervisor, SupervisorRef
from spaceone.plugin.manager import PluginManager, SupervisorManager, SupervisorRefManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class SupervisorService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self._supervisor_mgr: SupervisorManager = self.locator.get_manager('SupervisorManager')
        self._supervisor_ref_mgr: SupervisorRefManager = self.locator.get_manager('SupervisorRefManager')

    @transaction
    @check_required(['name', 'hostname', 'domain_id'])
    def publish(self, params):
        _LOGGER.debug(f'[publish] params: {params}')
        plugin_mgr: PluginManager = self.locator.get_manager('PluginManager')

        domain_id = params['domain_id']
        # get supervisor
        if 'user_id' in params:
            del params['user_id']

        try:
            # unique: hostname + name
            supervisor = self._supervisor_mgr.get_by_hostname(params['hostname'], domain_id)
        except ERROR_NOT_FOUND:
            # create new supervisor
            supervisor = self._supervisor_mgr.create(params)
            ###############################
            # East EGG for Automatic Test
            ###############################
            if params['name'] == 'root':
                self._supervisor_mgr.update({'supervisor_id': supervisor.supervisor_id, 'is_public': True, 'domain_id': domain_id})

        if supervisor:
            plugins_info = params.get('plugin_info', [])
            print(f'[publish] plugin_info: {plugins_info}')
            for plugin in plugins_info:
                # Update State (XXXX -> ACTIVE)
                # Update endpoint (grpc://xxxx)
                # There may be no plugin at DB (maybe deleted, or supervisor's garbage)
                #self._plugin_mgr.update_plugin(plugin)
                _LOGGER.debug(f'[publish] plugin={plugin}')
                try:
                    plugin_mgr.update_plugin_state(plugin['plugin_id'],
                                                   plugin['version'],
                                                   plugin['state'],
                                                   plugin['endpoint'],
                                                   supervisor.supervisor_id)
                except Exception as e:
                    _LOGGER.error(f'[publish] e={e}')
                    _LOGGER.warning(f'[publish] Failed update plugin.state:{plugin["state"]}')
        else:
            # There is no plugin_info
            supervisor = self._supervisor_mgr.create(params)


        return supervisor

    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def register(self, params):
        domain_id = params['domain_id']
        _LOGGER.debug(f'[register] params: {params}')

        # TODO: Should I validate supervisor_id?
        return self._supervisor_mgr.register(params['supervisor_id'], domain_id)

    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def update(self, params):
        domain_id = params['domain_id']
        _LOGGER.debug(f'[update] params: {params}')


        # TODO: Should I validate supervisor_id?
        return self._supervisor_mgr.update(params)


    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def deregister(self, params):
        domain_id = params['domain_id']
        _LOGGER.debug(f'[deregister] supervisor_id: {params["supervisor_id"]}')
        self._supervisor_mgr.delete(params['supervisor_id'], domain_id)

    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def enable(self, params):
        domain_id = params['domain_id']
        _LOGGER.debug(f'[enable] supervisor_id: {params["supervisor_id"]}')
        return self._supervisor_mgr.enable(params['supervisor_id'], domain_id)

    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def disable(self, params):
        domain_id = params['domain_id']
        _LOGGER.debug(f'[disable] supervisor_id: {params["supervisor_id"]}')
        return self._supervisor_mgr.disable(params['supervisor_id'], domain_id)

    @transaction
    @check_required(['supervisor_id', 'plugin_id', 'version', 'domain_id'])
    def recover_plugin(self, params):
        """ Recover plugin if exist
        """
        supervisor_id = params['supervisor_id']
        domain_id = params['domain_id']

        try:
            supervisor = self._get_supervisor_by_id(supervisor_id, domain_id)
        except Exception as e:
            _LOGGER.info(f'[recover_plugin] No matched supervisor, \
                                supervisor_id: {supervisor_id}, domain_id: {domain_id}')
            raise ERROR_NOT_SUPPORT_RECOVER_PLUGIN(supervisor_id=supervisor_id)
        
        plugin_id = params['plugin_id']
        version = params['version']

        # Get plugin_info
        plugin_mgr: PluginManager = self.locator.get_manager('PluginManager')
        
        plugin_vo = plugin_mgr.get(supervisor_id, domain_id, plugin_id, version)

        # Get endpoint
        endpoint = plugin_vo.endpoint
        plugin_vo = plugin_mgr.make_reprovision(plugin_id, version)
        return plugin_vo


    @transaction
    @check_required(['supervisor_id', 'domain_id'])
    def get(self, params):
        """ Get PluginManager

        Args:
            params:
                - plugin_manager_id
                - domain_id (from metadata)
        Returns:
            PluginManagerData
        """
    @transaction
    @check_required(['domain_id'])
    @append_query_filter(filter_keys=['supervisor_id', 'name', 'is_public', 'hostname', 'domain_id'])
    def list_supervisors(self, params):
        query = params.get('query', {})
        return self._supervisor_mgr.list_supervisors(query)

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(filter_keys=['supervisor_id', 'hostname', 'plugin_id', 'version', 'state', 'endpoint'])
    def list_plugins(self, params):
        """ 
        Find all plugins (either supervisor or supervisor_ref)

        This function is usually called by Supervisor for sync plugins
        """

        # Request from supervisor has no supervisor_id
        supervisor_id = params.get('supervisor_id', None)
        hostname = params.get('hostname', None)
        domain_id = params['domain_id']

        if supervisor_id is None and hostname is None:  
            raise ERROR_REQUIRED_PARAMETER(key='supervisor_id | hostname')

        query = params.get('query', {})

        # Find Supevisor
        supervisor = self._find_supervisor(supervisor_id, hostname, domain_id)


        if isinstance(supervisor, Supervisor):
            # Find all plugins from this supervisor
            return self._supervisor_mgr.list_plugins(query)

        if isinstance(supervisor, SupervisorRef):
            # SupervisorRef Model
            raise ERROR_NOT_SUPPORT_LIST_PLUGINS(params['supervisor_id'])

    def _get_supervisor_by_id(self, supervisor_id, domain_id):
        """ Find Supervisor with supervisor_id
        Only find at Supervisor (not supervisor_ref)
        Return may be Supervisor
        """
        return self._supervisor_mgr.get_by_id(supervisor_id, domain_id)

    def _find_supervisor(self, supervisor_id, hostname, domain_id):
        """ Return supervisor from supervisor or supervisor_ref
        """
        try:
            resp = self._supervisor_mgr.get_by_id_or_hostname(supervisor_id, hostname, domain_id)
            return resp
        except Exception as e:
            _LOGGER.debug(f'[_find_supervisor] not found at supervisor, \
                                supervisor_id: {supervisor_id}, domain_id: {domain_id}')

        try:
            resp = self._supervisor_ref_mgr.get_by_id(supervisor_id, domain_id)
            return resp
        except Exception as e:
            _LOGGER.debug(f'[_find_supervisor] not found at supervisor_ref, \
                                supervisor_id: {supervisor_id}, domain_id: {domain_id}')

        raise ERROR_NO_POSSIBLE_SUPERVISOR(params=supervisor_id)

def _query_supervisor(supervisor_id, domain_id):
    return {
        'filter': [
            {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            },
            {
                'k': 'supervisor_id',
                'v': supervisor_id,
                'o': 'eq'
            }
        ]
    }
