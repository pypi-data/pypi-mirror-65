import logging

from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.secret_connector import SecretConnector

_LOGGER = logging.getLogger(__name__)


class SecretManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_connector: SecretConnector = self.locator.get_connector('SecretConnector')

    def list_secrets(self, query, domain_id):
        return self.secret_connector.list_secrets(query, domain_id)

    def get_secret_data(self, secret_id, domain_id):
        return self.secret_connector.get_secret_data(secret_id, domain_id)

    def get_plugin_secret_data(self, secret_id, supported_schema, domain_id):
        secret_query = self._make_query(supported_schema, secret_id=secret_id)
        response = self.list_secrets(secret_query, domain_id)

        if response['total_count'] == 0:
            raise ERROR_NOT_FOUND(key='plugin_info.secret_id', value=secret_id)

        return self.get_secret_data(secret_id, domain_id)

    def get_resource_secret_data(self, provider, resource_id, resource_secrets, supported_schema, domain_id):
        secret_query = self._make_query(supported_schema, provider=provider, resource_secrets=resource_secrets)
        response = self.list_secrets(secret_query, domain_id)

        if response['total_count'] == 0:
            raise ERROR_RESOURCE_SECRETS_NOT_EXISTS(resource_id=resource_id)

        secret_id = response['results'][0]
        return self.get_secret_data(secret_id, domain_id)

    def get_plugin_secret(self, plugin_id, secret_id, provider, capability, domain_id):
        use_resource_secret = capability.get('use_resource_secret', False)
        supported_schema = capability.get('supported_schema', [])

        self._check_plugin_secret(use_resource_secret, secret_id, provider)

        if use_resource_secret:
            secret_query = self._make_query(supported_schema, provider=provider)
        else:
            secret_query = self._make_query(supported_schema, secret_id=secret_id)

        response = self.list_secrets(secret_query, domain_id)

        if response['total_count'] == 0:
            if use_resource_secret:
                raise ERROR_SUPPORTED_SECRETS_NOT_EXISTS(plugin_id=plugin_id, provider=provider)
            else:
                raise ERROR_NOT_FOUND(key='plugin_info.secret_id', value=secret_id)

        secret_id = response['results'][0]

        return self.get_secret_data(secret_id, domain_id)

    @staticmethod
    def _check_plugin_secret(use_resource_secret, secret_id, provider):
        if use_resource_secret:
            if provider is None:
                raise ERROR_REQUIRED_PARAMETER(key='plugin_info.provider')
        else:
            if secret_id is None:
                raise ERROR_REQUIRED_PARAMETER(key='plugin_info.secret_id')

    @staticmethod
    def _make_query(supported_schema, **kwargs):
        secret_id = kwargs.get('secret_id')
        provider = kwargs.get('provider')
        resource_secrets = kwargs.get('resource_secrets')

        query = {
            'filter': []
        }

        if supported_schema:
            query['filter'].append({
                'k': 'schema',
                'v': supported_schema,
                'o': 'in'
            })

        if secret_id:
            query['filter'].append({
                'k': 'secret_id',
                'v': secret_id,
                'o': 'eq'
            })

        if provider:
            query['filter'].append({
                'k': 'provider',
                'v': provider,
                'o': 'eq'
            })

        if resource_secrets:
            query['filter'].append({
                'k': 'secret_id',
                'v': resource_secrets,
                'o': 'in'
            })

        return query
