# -*- coding: utf-8 -*-
import logging

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

    def query_resources(self, query, vo=False):
        """
        if vo is True, return VO instead of filtered result
        """
        query['only'] = ['network_policy_id']
        resources = []
        network_policy_vos, total_count = self.list_network_policies(query)

        if vo:
            return network_policy_vos, total_count

        for network_policy_vo in network_policy_vos:
            resources.append({'network_policy_id': network_policy_vo.network_policy_id})

        return resources, total_count