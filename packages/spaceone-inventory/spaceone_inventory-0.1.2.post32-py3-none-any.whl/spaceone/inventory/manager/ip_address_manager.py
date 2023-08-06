# -*- coding: utf-8 -*-
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.model.ip_address_model import IPAddress

_LOGGER = logging.getLogger(__name__)


class IPManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip_model: IPAddress = self.locator.get_model('IPAddress')

    def create_ip(self, params):
        def _rollback(ip_vo):
            _LOGGER.info(f'[ROLLBACK] Cancel Create IP : {ip_vo.ip_address}')
            ip_vo.delete()

        ip_vo: IPAddress = self.ip_model.create(params)
        self.transaction.add_rollback(_rollback, ip_vo)

        return ip_vo

    def update_ip_by_vo(self, params, ip_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Data : {old_data.get("ip_address")}')
            ip_vo.update(old_data)

        self.transaction.add_rollback(_rollback, ip_vo.to_dict())

        return ip_vo.update(params)

    def allocate_ip(self, params):
        params['state'] = 'ALLOCATED'
        return self.create_ip(params)

    def reserve_ip(self, params):
        params['state'] = 'RESERVED'
        return self.create_ip(params)

    def release_ip(self, ip, domain_id, subnet_vo):
        self.release_ip_by_vo(self.get_ip_by_subnet_vo(ip, domain_id, subnet_vo))

    def get_ip_by_subnet_vo(self, ip, domain_id, subnet_vo):
        return self.ip_model.get(ip_address=ip, subnet=subnet_vo, domain_id=domain_id)

    def list_ips(self, query):
        return self.ip_model.query(**query)

    def create_by_collector(self, params, collector_id, collect_state):
        # TODO: Data Version Control System
        params['collect_info'] = {
            'state': collect_state,
            'collectors': [collector_id]
        }

        return self.create_ip(params)

    def update_by_collector(self, params, ip_vo, collector_id, collect_state):
        # TODO: Data Version Control System
        collectors = ip_vo.collect_info.get('collectors', [])

        if collector_id not in collectors:
            collectors.append(collector_id)

        params['collect_info'] = {
            'state': collect_state,
            'collectors': collectors
        }

        return self.update_ip_by_vo(params, ip_vo)

    @staticmethod
    def release_ip_by_vo(ip_vo):
        ip_vo.delete()

    def query_resources(self, query, vo=False):
        """
        if vo is True, return VO instead of filtered result
        """
        query['only'] = ['ip_address', 'subnet']
        resources = []
        ip_vos, total_count = self.list_ips(query)

        if vo:
            return ip_vos, total_count

        for ip_vo in ip_vos:
            resources.append({'ip_address': ip_vo.ip_address, 'subnet_id': ip_vo.subnet.subnet_id})

        return resources, total_count