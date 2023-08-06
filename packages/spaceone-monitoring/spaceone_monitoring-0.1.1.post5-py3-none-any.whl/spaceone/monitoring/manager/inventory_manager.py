import logging

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.inventory_connector import InventoryConnector

_LOGGER = logging.getLogger(__name__)

_DEFAULT_REFERENCE_KEY = 'reference.resource_id'
_GET_RESOURCE_METHODS = {
    'inventory.Server': 'list_servers',
    'inventory.CloudService': 'list_cloud_services',
}
_RESOURCE_KEYS = {
    'inventory.Server': 'server_id'
}


class InventoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory_connector: InventoryConnector = self.locator.get_connector('InventoryConnector')

    def list_resources(self, resources, resource_type, reference_keys, domain_id):
        reference_key = self._get_reference_key(resource_type, reference_keys)
        query = self._make_query(resource_type, resources, reference_key)
        get_method = _GET_RESOURCE_METHODS[resource_type]

        response = getattr(self.inventory_connector, get_method)(query, domain_id)
        return self._change_resources_info(resource_type, response)

    def get_resource_key(self, resource_type, resource_info, reference_keys):
        reference_key = self._get_reference_key(resource_type, reference_keys)
        return utils.get_dict_value(resource_info, reference_key)

    @staticmethod
    def _change_resources_info(resource_type, response):
        resource_key = _RESOURCE_KEYS[resource_type]
        resources_info = {}
        for resource_info in response['results']:
            resource_id = resource_info[resource_key]
            resources_info[resource_id] = resource_info

        return resources_info

    @staticmethod
    def _make_query(resource_type, resources, reference_key):
        resource_key = _RESOURCE_KEYS[resource_type]
        return {
            'filter': [{
                'k': resource_key,
                'v': resources,
                'o': 'in'
            }],
            'only': [resource_key, reference_key, 'collection_info.secrets']
        }

    @staticmethod
    def _get_reference_key(resource_type: str, reference_keys: list) -> dict:
        reference_key = _DEFAULT_REFERENCE_KEY

        for key in reference_keys:
            if resource_type == key['resource_type']:
                reference_key = key['reference_key']
                break

        return reference_key
