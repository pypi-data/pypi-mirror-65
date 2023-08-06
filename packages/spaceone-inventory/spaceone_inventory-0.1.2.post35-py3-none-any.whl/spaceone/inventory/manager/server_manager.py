import logging

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.inventory.model.server_model import Server
from spaceone.inventory.error import *

_LOGGER = logging.getLogger(__name__)


class ServerManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_model: Server = self.locator.get_model('Server')

    def create_server(self, params):
        def _rollback(server_vo):
            _LOGGER.info(f'[ROLLBACK] Delete Server : {server_vo.name} ({server_vo.server_id})')
            server_vo.terminate()

        server_vo: Server = self.server_model.create(params)
        self.transaction.add_rollback(_rollback, server_vo)

        return server_vo

    def update_server(self, params):
        server_vo: Server = self.get_server(params['server_id'], params['domain_id'])
        return self.update_server_by_vo(params, server_vo)

    def update_server_by_vo(self, params, server_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Server Data : {old_data["name"]} ({old_data["server_id"]})')
            server_vo.update(old_data)

        self.transaction.add_rollback(_rollback, server_vo.to_dict())

        return server_vo.update(params)

    def delete_server(self, server_id, domain_id):
        server_vo: Server = self.get_server(server_id, domain_id)
        server_vo.delete()

    def get_server(self, server_id, domain_id):
        return self.server_model.get(server_id=server_id, domain_id=domain_id)

    def list_servers(self, query):
        result = self.server_model.query(**query)
        return result

    def query_resources(self, query, only):
        dotted_key = only[0]
        values = []
        secrets = []
        query['only'] = only + ['collection_info.secrets']

        vos, total_count = self.list_servers(query)

        for vo in vos:
            data = vo.to_dict()
            value = utils.get_dict_value(data, dotted_key)
            if value:
                values.append(value)

            secrets = secrets + utils.get_dict_value(data, 'collection_info.secrets', [])

        return list(set(values)), list(set(secrets))

    def find_resources(self, query):
        key = 'server_id'
        query['only'] = [key]

        resources = []
        vos, total_count = self.list_servers(query)

        for vo in vos:
            resources.append({key: getattr(vo, key)})

        return resources, total_count
