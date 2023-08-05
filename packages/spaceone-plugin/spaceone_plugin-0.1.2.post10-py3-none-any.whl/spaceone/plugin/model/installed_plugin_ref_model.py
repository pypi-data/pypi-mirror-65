# -*- coding: utf-8 -*-

__all__ = ['InstalledPluginRef']

from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel
from spaceone.plugin.model.supervisor_ref_model import SupervisorRef

class InstalledPluginRef(MongoModel):
    supervisor_id = StringField(max_length=255, required=True, null=False)
    domain_id = StringField(max_length=255, required=True, null=False)
    plugin_id = StringField(max_length=255, required=True, null=False)
    version = StringField(max_length=255, required=True, null=False)
    supervisor = ReferenceField('SupervisorRef', required=True, null=False)

    meta = {
        'db_alias': 'default',
        'updatable_fields': [
        ],
        'exact_fields': [
            'supervisor_id',
            'domain_id',
            'plugin_id',
            'version'
        ],
        'minimal_fields': [
            'supervisor_id',
            'domain_id'
            'plugin_id',
            'version'
        ],
        'ordering': ['supervisor_id'],
        'indexes': [
            'plugin_id'
        ]
    }

