from spaceone.core import utils
from spaceone.core.error import *


class ResourceFinder(object):

    resource_keys: list = None
    query_method = None

    def query_resources(self, query, change_rules):
        secrets = []
        only = ['collection_info.secrets']
        change_values = {}
        change_key_map = {}
        for rule in change_rules:
            resource_key = rule['resource_key']
            change_key = rule['change_key']

            change_key_map[resource_key] = change_key
            change_values[change_key] = []
            only.append(resource_key)

        vos, total_count = getattr(self, self.query_method)(query)

        for vo in vos:
            data = vo.to_dict()
            for resource_key, change_key in change_key_map.items():
                value = utils.get_dict_value(data, resource_key)
                if value:
                    change_values[change_key].append(value)

            secrets = secrets + utils.get_dict_value(data, 'collection_info.secrets', [])

        for key, values in change_values.items():
            change_values[key] = list(set(values))

        return change_values, list(set(secrets))

    def find_resources(self, query):
        self._check_resource_finder_state()
        query['only'] = self.resource_keys

        resources = []
        vos, total_count = getattr(self, self.query_method)(query)

        for vo in vos:
            data = {}
            for key in self.resource_keys:
                data[key] = getattr(vo, key)

            resources.append(data)

        return resources, total_count

    def _check_resource_finder_state(self):
        if not (self.resource_keys and self.query_method):
            raise ERROR_UNKNOWN(message='ResourceFinder is not set.')

        if getattr(self, self.query_method, None) is None:
            raise ERROR_UNKNOWN(message='ResourceFinder is not set.')
