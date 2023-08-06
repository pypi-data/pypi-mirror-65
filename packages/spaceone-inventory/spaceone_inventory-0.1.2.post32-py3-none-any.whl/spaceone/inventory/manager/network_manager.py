# -*- coding: utf-8 -*-
import logging

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

    def query_resources(self, query, vo=False):
        """
        if vo is True, return VO instead of filtered result
        """
        query['only'] = ['network_id']
        resources = []
        network_vos, total_count = self.list_networks(query)

        if vo:
            return network_vos, total_count

        for network_vo in network_vos:
            resources.append({'network_id': network_vo.network_id})

        return resources, total_count