# -*- coding: utf-8 -*-
from spaceone.core.service import *
from spaceone.inventory.manager.cloud_service_type_manager import CloudServiceTypeManager
from spaceone.inventory.manager.collection_data_manager import CollectionDataManager
from spaceone.inventory.error import *


@authentication_handler
@authorization_handler
@event_handler
class CloudServiceTypeService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.cloud_svc_type_mgr: CloudServiceTypeManager = self.locator.get_manager('CloudServiceTypeManager')

    @transaction
    @check_required(['name', 'provider', 'group', 'domain_id'])
    def create(self, params):
        """
        Args:
            params (dict): {
                    'name': 'str',
                    'group': 'str',
                    'provider': 'str',
                    'data_source': 'list',
                    'labels': 'list,
                    'tags': 'dict',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        collection_data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        domain_id = params['domain_id']

        collector_id = self.transaction.get_meta('collector_id')
        service_account_id = self.transaction.get_meta('service_account_id')
        secret_id = self.transaction.get_meta('secret_id')
        job_id = self.transaction.get_meta('job_id')

        params['collection_info'] = collection_data_mgr.create_new_history(params,
                                                                           domain_id,
                                                                           collector_id,
                                                                           service_account_id,
                                                                           secret_id,
                                                                           exclude_keys=['domain_id'])

        return self.cloud_svc_type_mgr.create_cloud_service_type(params)

    @transaction
    @check_required(['cloud_service_type_id', 'domain_id'])
    def update(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'data_source': 'list',
                    'labels': 'list',
                    'tags': 'dict',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        collection_data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        domain_id = params['domain_id']

        collector_id = self.transaction.get_meta('collector_id')
        service_account_id = self.transaction.get_meta('service_account_id')
        secret_id = self.transaction.get_meta('secret_id')
        job_id = self.transaction.get_meta('job_id')

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                           domain_id)

        params = collection_data_mgr.exclude_data_by_pinned_keys(params, cloud_svc_type_vo.collection_info)
        params = collection_data_mgr.exclude_data_by_history(params,
                                                             cloud_svc_type_vo.to_dict(),
                                                             domain_id,
                                                             cloud_svc_type_vo.collection_info,
                                                             collector_id,
                                                             service_account_id,
                                                             secret_id,
                                                             exclude_keys=['cloud_service_type_id', 'domain_id'])

        return self.cloud_svc_type_mgr.update_cloud_service_type_by_vo(params, cloud_svc_type_vo)

    @transaction
    @check_required(['cloud_service_id', 'keys', 'domain_id'])
    def pin_data(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'keys': 'list',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_vo (object)

        """

        collection_data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                           params['domain_id'])

        params['collection_info'] = collection_data_mgr.update_pinned_keys(params['keys'],
                                                                           cloud_svc_type_vo.collection_info)

        return self.cloud_svc_type_mgr.update_cloud_service_by_vo(params, cloud_svc_type_vo)

    @transaction
    @check_required(['cloud_service_type_id', 'domain_id'])
    def delete(self, params):

        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'domain_id': 'str'
                }

        Returns:
            None

        """

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                    params['domain_id'])

        self.cloud_svc_type_mgr.delete_cloud_service_type_by_vo(cloud_svc_type_vo)

    @transaction
    @check_required(['cloud_service_type_id', 'domain_id'])
    def get(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        return self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'], params['domain_id'])

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['cloud_service_type_id', 'name', 'provider', 'group', 'domain_id'])
    def list(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'name': 'str',
                    'group': 'str',
                    'provider': 'str',
                    'include_cloud_service_count': 'boot',
                    'domain_id': 'str',
                    'query': 'dict'
                }

        Returns:
            results (list)
            total_count (int)

        """

        return self.cloud_svc_type_mgr.list_cloud_service_types(params.get('query', {}),
                                                                params.get('include_cloud_service_count', False))
