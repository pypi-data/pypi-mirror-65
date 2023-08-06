import logging

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.inventory.lib import rule_matcher
from spaceone.inventory.model.network_policy_model import NetworkPolicy

_LOGGER = logging.getLogger(__name__)


class NetworkPolicyManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.npolicy_model: NetworkPolicy = self.locator.get_model('NetworkPolicy')

    def create_network_policy(self, params):
        def _rollback(npolicy_vo):
            _LOGGER.info(f'[ROLLBACK] Delete network policy : {npolicy_vo.name} ({npolicy_vo.network_policy_id})')
            npolicy_vo.delete()

        npolicy_vo: NetworkPolicy = self.npolicy_model.create(params)
        self.transaction.add_rollback(_rollback, npolicy_vo)

        return npolicy_vo

    def update_network_policy(self, params):
        return self.update_network_policy_by_vo(params,
                                                self.get_network_policy(params.get('network_policy_id'),
                                                                        params.get('domain_id')))

    def update_network_policy_by_vo(self, params, network_policy_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Data : {old_data.get("name")} ({old_data.get("network_policy_id")})')
            network_policy_vo.update(old_data)

        self.transaction.add_rollback(_rollback, network_policy_vo.to_dict())

        return network_policy_vo.update(params)

    def delete_network_policy(self, npolicy_id, domain_id):
        self.delete_network_policy_by_vo(self.get_network_policy(npolicy_id, domain_id))

    def get_network_policy(self, network_policy_id, domain_id):
        return self.npolicy_model.get(network_policy_id=network_policy_id, domain_id=domain_id)

    def list_network_policies(self, query):
        return self.npolicy_model.query(**query)

    @staticmethod
    def delete_network_policy_by_vo(npolicy_vo):
        npolicy_vo.delete()

    def query_resources(self, query, only):
        dotted_key = only[0]
        values = []
        secrets = []
        query['only'] = only + ['collection_info.secrets']

        vos, total_count = self.list_network_policies(query)

        for vo in vos:
            data = vo.to_dict()
            value = utils.get_dict_value(data, dotted_key)
            if value:
                values.append(value)

            secrets = secrets + utils.get_dict_value(data, 'collection_info.secrets', [])

        return list(set(values)), list(set(secrets))

    def find_resources(self, query):
        key = 'network_policy_id'
        query['only'] = [key]

        resources = []
        vos, total_count = self.list_network_policies(query)

        for vo in vos:
            resources.append({key: getattr(vo, key)})

        return resources, total_count
