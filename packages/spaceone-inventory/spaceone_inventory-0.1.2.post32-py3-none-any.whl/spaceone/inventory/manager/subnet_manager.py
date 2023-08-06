# -*- coding: utf-8 -*-
import logging

from spaceone.core.manager import BaseManager
from spaceone.inventory.model.subnet_model import Subnet

_LOGGER = logging.getLogger(__name__)


class SubnetManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subnet_model: Subnet = self.locator.get_model('Subnet')

    def create_subnet(self, params):
        def _rollback(subnet_vo):
            _LOGGER.info(f'[ROLLBACK] Delete subnet : {subnet_vo.subnet_id}')
            subnet_vo.delete()

        subnet_vo: Subnet = self.subnet_model.create(params)
        self.transaction.add_rollback(_rollback, subnet_vo)

        return subnet_vo

    def update_subnet(self, params):
        return self.update_subnet_by_vo(params,
                                        self.get_subnet(params.get('subnet_id'), params.get('domain_id')))

    def update_subnet_by_vo(self, params, subnet_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Data : {old_data.get("subnet_id")}')
            subnet_vo.update(old_data)

        self.transaction.add_rollback(_rollback, subnet_vo.to_dict())

        subnet_vo = subnet_vo.update(params)
        return subnet_vo

    def delete_subnet(self, subnet_id, domain_id):
        self.delete_subnet_by_vo(self.get_subnet(subnet_id, domain_id))

    def get_subnet(self, subnet_id, domain_id):
        return self.subnet_model.get(subnet_id=subnet_id, domain_id=domain_id)

    def list_subnets(self, query):
        return self.subnet_model.query(**query)

    @staticmethod
    def delete_subnet_by_vo(subnet_vo):
        subnet_vo.delete()

    def query_resources(self, query, vo=False):
        """
        if vo is True, return VO instead of filtered result
        """
        query['only'] = ['subnet_id']
        resources = []
        subnet_vos, total_count = self.list_subnets(query)

        if vo:
            return subnet_vos, total_count

        for subnet_vo in subnet_vos:
            resources.append({'subnet_id': subnet_vo.subnet_id})

        return resources, total_count
