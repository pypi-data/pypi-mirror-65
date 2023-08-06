import logging

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.inventory.lib import rule_matcher
from spaceone.inventory.model.network_model import Network

_LOGGER = logging.getLogger(__name__)


class NetworkManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.network_model: Network = self.locator.get_model('Network')

    def create_network(self, params):
        def _rollback(network_vo):
            _LOGGER.info(f'[ROLLBACK] Delete network : {network_vo.network_id}')
            network_vo.delete()

        network_vo: Network = self.network_model.create(params)
        self.transaction.add_rollback(_rollback, network_vo)

        return network_vo

    def update_network(self, params):
        return self.update_network_by_vo(params,
                                         self.get_network(params.get('network_id'), params.get('domain_id')))

    def update_network_by_vo(self, params, network_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Data : {old_data.get("network_id")}')
            network_vo.update(old_data)

        self.transaction.add_rollback(_rollback, network_vo.to_dict())

        return network_vo.update(params)

    def delete_network(self, network_id, domain_id):
        self.delete_network_vo(self.get_network(network_id, domain_id))

    def get_network(self, network_id, domain_id):
        return self.network_model.get(network_id=network_id, domain_id=domain_id)

    def list_networks(self, query):
        return self.network_model.query(**query)

    @staticmethod
    def delete_network_vo(network_vo):
        network_vo.delete()

    def query_resources(self, query, only):
        dotted_key = only[0]
        values = []
        secrets = []
        query['only'] = only + ['collection_info.secrets']

        vos, total_count = self.list_networks(query)

        for vo in vos:
            data = vo.to_dict()
            value = utils.get_dict_value(data, dotted_key)
            if value:
                values.append(value)

            secrets = secrets + utils.get_dict_value(data, 'collection_info.secrets', [])

        return list(set(values)), list(set(secrets))

    def find_resources(self, query):
        key = 'network_id'
        query['only'] = [key]

        resources = []
        vos, total_count = self.list_networks(query)

        for vo in vos:
            resources.append({key: getattr(vo, key)})

        return resources, total_count
