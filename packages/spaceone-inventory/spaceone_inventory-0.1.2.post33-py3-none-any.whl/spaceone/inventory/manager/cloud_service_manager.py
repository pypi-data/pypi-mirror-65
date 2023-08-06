import logging

from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.inventory.model.cloud_service_model import CloudService

_LOGGER = logging.getLogger(__name__)


class CloudServiceManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_svc_model: CloudService = self.locator.get_model('CloudService')

    def create_cloud_service(self, params):
        def _rollback(cloud_svc_vo):
            _LOGGER.info(
                f'[ROLLBACK] Delete Cloud Service : {cloud_svc_vo.provider} ({cloud_svc_vo.cloud_service_type})')
            cloud_svc_vo.delete(True)

        cloud_svc_vo: CloudService = self.cloud_svc_model.create(params)
        self.transaction.add_rollback(_rollback, cloud_svc_vo)

        return cloud_svc_vo

    def update_cloud_service(self, params):
        return self.update_cloud_service_by_vo(params,
                                               self.get_cloud_service(params['cloud_service_id'], params['domain_id']))

    def update_cloud_service_by_vo(self, params, cloud_svc_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Revert Data : {old_data.get("cloud_service_id")}')
            cloud_svc_vo.update(old_data)

        self.transaction.add_rollback(_rollback, cloud_svc_vo.to_dict())
        return cloud_svc_vo.update(params)

    def delete_cloud_service(self, cloud_service_id, domain_id):
        self.delete_cloud_service_by_vo(self.get_cloud_service(cloud_service_id, domain_id))

    def get_cloud_service(self, cloud_service_id, domain_id):
        return self.cloud_svc_model.get(cloud_service_id=cloud_service_id, domain_id=domain_id)

    def list_cloud_services(self, query):
        return self.cloud_svc_model.query(**query)

    @staticmethod
    def delete_cloud_service_by_vo(cloud_svc_vo):
        cloud_svc_vo.delete()

    def query_resources(self, query, only):
        dotted_key = only[0]
        values = []
        secrets = []
        query['only'] = only + ['collection_info.secrets']

        vos, total_count = self.list_cloud_services(query)

        for vo in vos:
            data = vo.to_dict()
            value = utils.get_dict_value(data, dotted_key)
            if value:
                values.append(value)

            secrets = secrets + utils.get_dict_value(data, 'collection_info.secrets', [])

        return list(set(values)), list(set(secrets))

    def find_resources(self, query):
        key = 'cloud_service_id'
        query['only'] = [key]

        resources = []
        vos, total_count = self.list_cloud_services(query)

        for vo in vos:
            resources.append({key: getattr(vo, key)})

        return resources, total_count
