# -*- coding: utf-8 -*-

import logging

from google.protobuf.json_format import MessageToDict

from spaceone.core import config
from spaceone.core import queue
from spaceone.core.error import *
from spaceone.core.manager import BaseManager
from spaceone.inventory.lib import rule_matcher

_LOGGER = logging.getLogger(__name__)

######################################################################
#    ************ Very Important ************
#
# This is resource map for collector
# If you add new service and manager for specific RESOURCE_TYPE,
# add here for collector
######################################################################
RESOURCE_MAP = {
    'SERVER': 'ServerManager',
    'NETWORK': 'NetworkManager',
    'NETWORK_POLICY': 'NetworkPolicyManager',
    'SUBNET': 'SubnetManager',
    'CLOUD_SERVICE': 'CloudServiceManager',
    'CLOUD_SERVICE_TYPE': 'CloudServiceTypeManager'
}

SERVICE_MAP = {
    'SERVER': 'ServerService',
    'NETWORK': 'NetworkService',
    'NETWORK_POLICY': 'NetworkService',
    'SUBNET': 'NetworkService',
    'CLOUD_SERVICE': 'CloudServiceService',
    'CLOUD_SERVICE_TYPE': 'CloudServiceTypeService'
}


#################################################
# Collecting Resource and Update DB
#################################################
class CollectingManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = {}       # Manager Mapping
        self.service = {}       # Service Mapping

    ##########################################################
    # collect
    #
    # links: https://pyengine.atlassian.net/wiki/spaces/CLOUD/pages/682459145/3.+Collector+Rule+Management
    #
    ##########################################################
    def collecting_resources(self, plugin_info, secret_id, filters, domain_id, **kwargs):
        """ This is single call of real plugin with endpoint

        All parameter should be primitive type, not object.
        Because this method will be executed by worker.
        Args:
            plugin_info(dict)
            kwargs: {
                'job_id': 'str',
            }
        """

        # Check Job State first, if job state is canceled, stop process
        job_mgr = self.locator.get_manager('JobManager')
        if job_mgr.is_canceled(kwargs['job_id'], domain_id):
            raise ERROR_COLLECT_CANCELED(job_id=kwargs['job_id'])

        # Create proper connector
        connector = self._get_connector(plugin_info, domain_id)

        # TODO:
        # Apply filter with collector_id, secret_id
        # Ask to Resource Owner (ex. ServerManager)
        try:
            collect_filter = self._get_collect_filter(filters, plugin_info)
        except Exception as e:
            _LOGGER.error(f'[collect_filter] {e}')
            _LOGGER.error(f'[collecting_resources] fail to make filter for Collect plugin, filter={filters}')
            raise ERROR_COLLECT_FILTER(plugin_info=plugin_info, filter=filters)

        # Get secret data
        try:
            secret_mgr = self.locator.get_manager('SecretManager')
            secret_data = secret_mgr.get_secret_data(secret_id, domain_id)
        except Exception as e:
            _LOGGER.error(f'[collecting_resources] fail to get secret_data: {secret_id}')
            raise ERROR_COLLECTOR_SECRET(plugin_info=plugin_info, param=secret_id)

        # Call method
        try:
            results = connector.collect(plugin_info['options'], secret_data.data, collect_filter)
            _LOGGER.debug('[collect] generator: %s' % results)
        except Exception as e:
            raise ERROR_COLLECTOR_COLLECTING(plugin_info=plugin_info, filters=collect_filter)

        try:
            self._process_results(results,
                                kwargs['job_id'],
                                kwargs['collector_id'],
                                secret_id,
                                domain_id
                            )
            job_mgr.decrease_remained_tasks(kwargs['job_id'], domain_id)
        except Exception as e:
            _LOGGER.error(f'[collecting_resources] {e}')

        return True

    def _process_results(self, results, job_id, collector_id, secret_id, domain_id):
        # update meta
        self.transaction.set_meta('job_id', job_id)
        self.transaction.set_meta('collector_id', collector_id)
        self.transaction.set_meta('secret_id', secret_id)
        # Service Account ID
        for res in results:
            try:
                params = {
                    'domain_id': domain_id,
                    'job_id': job_id
                }
                self._process_single_result(res, params)
            except Exception as e:
                _LOGGER.error(f'[_process_results] failed single result {e}')

    def _process_single_result(self, result, params):
        """ Process single resource (Add/Update)
            Args:
                result (message): resource from collector
                params (dict): {
                    'domain_id': 'str',
                    'job_id': 'str'
                }
        """
        domain_id = params['domain_id']
        resource_type = result.resource_type
        resource = MessageToDict(result, preserving_proto_field_name=True)
        data = resource['resource']
        data['domain_id'] = domain_id

        _LOGGER.debug(f'[_process_single_result] {resource_type}')
        (svc, mgr) = self._get_resource_map(resource_type)

        match_rules = resource.get('match_rules', {})
        try:
            res_info, total_count = self.query_with_match_rules(data,
                                                                match_rules,
                                                                domain_id,
                                                                mgr
                                                                )
            _LOGGER.debug(f'[_process_single_result] matched resources count = {total_count}')
        except Exception as e:
            _LOGGER.error(f'[_process_single_result] failed to match: {e}')
            _LOGGER.warning(f'[_process_single_result] assume new resource, create')
            total_count = 0

        job_mgr = self.locator.get_manager('JobManager')
        try:
            if total_count == 0:
                # Create
                _LOGGER.debug('[_process_single_result] Create resource.')
                res_msg = svc.create(data)
                job_mgr.increase_created_count(params['job_id'], domain_id)
            elif total_count == 1:
                # Update
                _LOGGER.debug('[_process_single_result] Update resource.')
                data.update(res_info[0])
                res_msg = svc.update(data)
                job_mgr.increase_updated_count(params['job_id'], domain_id)
            elif total_count > 1:
                # Ambiguous
                _LOGGER.debug(f'[_process_single_result] Too many resources matched. (count={total_count})')
                _LOGGER.warning(f'[_process_single_result] match_rules: {match_rules}')
        except Exception as e:
            _LOGGER.debug(f'[_process_single_result] service error: {svc}, {e}')

    def _get_resource_map(self, resource_type):
        """ Base on resource type

        Returns: (service, manager)
        """
        if resource_type not in RESOURCE_MAP:
            raise ERROR_UNSUPPORTED_RESOURCE_TYPE(resource_type=resource_type)
        if resource_type not in SERVICE_MAP:
            raise ERROR_UNSUPPORTED_RESOURCE_TYPE(resource_type=resource_type)

        # Get proper manager
        if resource_type not in self.manager:
            mgr = self.locator.get_manager(RESOURCE_MAP[resource_type])
            self.manager[resource_type] = mgr
        else:
            mgr = self.manager[resource_type]

        # Get proper service
        if resource_type not in self.service:
            svc = self.locator.get_service(SERVICE_MAP[resource_type], metadata=self.transaction.meta)
            self.service[resource_type] = svc
        else:
            svc = self.service[resource_type]
        return (svc, mgr)

    ######################
    # Internal
    ######################
    def _get_connector(self, plugin_info, domain_id, **kwargs):
        """ Find proper connector(plugin)

        Returns: connector (object)
        """
        connector = self.locator.get_connector('CollectorPluginConnector')
        # get endpoint
        endpoint = self._get_endpoint(plugin_info, domain_id)
        _LOGGER.debug('[collect] endpoint: %s' % endpoint)
        connector.initialize(endpoint)

        return connector

    def _get_endpoint(self, plugin_info, domain_id):
        """ get endpoint from plugin_info

        Args:
            plugin_info (dict) : {
                'plugin_id': 'str',
                'version': 'str',
                'options': 'dict',
                'secret_id': 'str',
                'secret_group_id': 'str',
                'provider': 'str',
                'capabilities': 'dict'
                }
            domain_id (str)

        Returns: Endpoint Object

        """
        # Call Plugin Service
        plugin_id = plugin_info['plugin_id']
        version = plugin_info['version']

        plugin_connector = self.locator.get_connector('PluginConnector')
        # TODO: label match

        endpoint = plugin_connector.get_plugin_endpoint(plugin_id, version, domain_id)
        return endpoint

    def query_with_match_rules(self, resource, match_rules, domain_id, mgr):
        """ match resource based on match_rules

        Args:
            resource: ResourceInfo(Json) from collector plugin
            match_rules:
                ex) {1:['data.vm.vm_id'], 2:['zone_id', 'data.ip_addresses']}

        Return:
            resource_id : resource_id for resource update (ex. {'server_id': 'server-xxxxxx'})
            True: can not determine resources (ambiguous)
            False: no matched
        """

        found_resource = None
        total_count = 0

        match_rules = rule_matcher.dict_key_int_parser(match_rules)

        match_order = match_rules.keys()

        for order in sorted(match_order):
            query = rule_matcher.make_query(order, match_rules, resource, domain_id)
            _LOGGER.debug(f'[query_with_match_rules] query generated: {query}')
            found_resource, total_count = mgr.query_resources(query)
            if found_resource and total_count == 1:
                return found_resource, total_count

        return found_resource, total_count

    #####################################################
    # TODO: result of _get_collect_filter, and secret_id
    """ I want to know the founded result from _get_collect_filter must be related with secret_id
    If resource is not collected by this secret_id, I don't want to make collect call
    """
    def _get_collect_filter(self, filters, plugin_info, secret_id=None):
        """ Create new filters for Collect plugin's parameter
            filter_format(filters) -> new_filter

        Args:
            filter_format(list): filter_format from plugin.options.filter_format or None
            filters(dict): filters from Client request

        Returns:
            new_filter: new filters for Plugin(Collector) query

        Example:
            filter_format:
                'filter_format': [
                    {'key':'region_id', 'name':'Region', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
                    {'key':'zone_id', 'name':'Zone', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
                    {'key':'pool_id', 'name':'Pool', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
                    {'key':'server_id', 'name':'Server', 'type':'list', 'resource_type': 'SERVER', 'object_key': 'uuid', 'change_key': ['data.compute.instance_id', 'instance_id']},
                    {'key':'instance_id', 'name':'Instance ID', 'type':'list', 'resource_type': 'CUSTOM'},
                ]

            filters:
                {
                    'region_id': 'region-xxxxx',
                    'zone_id': 'zone-yyyyy',
                    'instance_id': ['i-zzzz', ...]]            # CUSTOM resource type
                }

            new_filter:
                {
                    'instance_id': ['i-123', 'i-2222', ...]
                }
        """

        filter_format = plugin_info.get('filter_format', None)
        if filter_format == None:
            return {}

        filter_format_by_key = {}
        # filter_format_by_key['zone_id'] = {'key':'zone_id', 'name':'Zone', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']}
        for item in filter_format:
            filter_format_by_key[item['key']] = item

        for filter_key, filter_value in filters.items():
            if filter_key not in filter_format_by_key:
                _LOGGER.error(f'[_get_collect_filter] unsupported filter_key: {filter_key}')
                # Strict error raise, for reducing too heavy requst
                raise ERROR_UNSUPPORTED_FILTER_KEY(key=filter_key, value=filter_value)

        query_filter, custom_keys = self._make_query_filter(filters, filter_format_by_key)
        _LOGGER.debug(f'[_get_collect_filter] query_filter: {query_filter}, custom_keys: {custom_keys}')

        query_per_resources = self._make_query_per_resources(query_filter, filter_format_by_key)
        _LOGGER.debug(f'[_get_collect_filter] query_per_resources: {query_per_resources}')

        result = self._search_resources(query_per_resources, filter_format_by_key)
        _LOGGER.debug(f'[_get_collect_filter] result: {result}')

        if len(custom_keys) > 0:
            result = self._append_custom_keys(result, custom_keys)
            _LOGGER.debug(f'[_get_collect_filter] result_with_custom_keys: {result}')

        return result

    def _make_query_filter(self, filters, filter_format_by_key):

        query_filter = {}
        """
        'region_id': [{'k': 'region_id', 'v': 'region-xxx', 'o': 'eq'}]
        'server_id': [{'k': 'server_id', 'v': 'server-yyyy', 'o': 'eq'} ....]
        ...
        """
        custom_keys = []
        # Foreach filter, we will find matched resource list
        for filter_key,filter_value in filters.items():
            # filter_key : region_id
            filter_element = filter_format_by_key[filter_key]
            _LOGGER.debug(f'[_make_query_filter] filter_element: {filter_element}')
            if filter_element['resource_type'] == 'CUSTOM':
                # DO NOT save CUSTOM key at query_filter
                custom_keys.append(k)
                continue

            # list of new_filter[key]
            v_list = query_filter.get(filter_key, [])
            if filter_element:
                # Ask to manager, is there any matched resource
                query = self._make_query_for_manager(filter_key, filter_value, filter_element)
                if isinstance(query, list) == False:
                    _LOGGER.error("LOGIC ERROR, _make_query_for_manager does not return list value: {query}")
                else:
                    v_list.extend(query)
            query_filter[filter_key] = v_list
        return query_filter, custom_keys

    def _make_query_per_resources(self, query_filter, filter_format_by_key):
        # Make query per Resource
        query_per_resources = {}
        """
        'SERVER': {
            'key': 'zone_id',
            'filter': [{'k': 'region_id', 'v': 'region-xxxx', 'o': 'eq'}],
            'filter_or': [{'k': 'server_id', 'v': 'server-yyyy', 'o': 'eq'}, ...]
            }
        """
        for query_key, query in query_filter.items():
                    res_type = filter_format_by_key[query_key]['resource_type']
                    query_string = query_per_resources.get(res_type, {'key': query_key, 'filter': [], 'filter_or': []})
                    if len(query) == 1:
                        query_string['filter'].extend(query)
                    elif len(query) > 1:
                        query_string['filter_or'].extend(query)
                    else:
                        _LOGGER.debug(f'[_get_collector_filter] wrong query: {query}')
                    query_per_resources[res_type] = query_string
        return query_per_resources

    def _search_resources(self, query_per_resources, filter_format_by_key):
        # Search Resource by Resource's Manager
        result = {}
        for res_type, query in query_per_resources.items():
            """ Example
            query: {'key': 'zone_id',
                    'filter': [
                            {'k': 'zone_id', 'v': 'zone-d710c1cb0ea7', 'o': 'eq'},
                            {'k': 'region_id', 'v': 'region-85445849c20c', 'o': 'eq'},
                            {'k': 'pool_id', 'v': 'pool-a1f35b107bb4', 'o': 'eq'}],
                    'filter_or': []}
            """
            _LOGGER.debug(f'[_search_resources] query: {query}')
            try:
                mgr = self.locator.get_manager(RESOURCE_MAP[res_type])
            except Exception as e:
                _LOGGER.error('########## NOTICE to Developer (bug) ###################################')
                _LOGGER.error(f'[_search_resources] Not found manager based on resource_type: {res_type}')
                _LOGGER.error(e)
                continue

            filter_element = filter_format_by_key[query['key']]
            change_key = filter_element['change_key']
            del query['key']

            # Ask to manager
            try:
                results, count = mgr.query_resources(query, vo=True)
            except Exception as e:
                _LOGGER.error('########## NOTICE to Developer (bug) ####################################')
                _LOGGER.error(f'{res_type} Manager has bug for query_resources functions')
                _LOGGER.error(e)
                results = []

            value_list = []
            for res in results:
                changed_value = self._get_value_from_vo(res, change_key[0])
                if changed_value:
                    value_list.append(changed_value)
                else:
                    _LOGGER.debug(f'Check Resource {res}')

            # Make new query
            if len(value_list) > 0:
                result.update({change_key[1]: value_list})
        return result

    def _append_custom_keys(self, result, custom_keys):
        for custom_key in custom_keys:
            _LOGGER.debug(f'[_append_custom_keys] append custom_key: {custom_key}')
            # TODO:fix 
            values = filters[custom_key]
            if isinstance(values, list):
                values = [values]
            v = result.get(custom_key, [])
            v.extend(values)
            result[custom_key] = v

        return result

    def _get_value_from_vo(self, vo, key):
        """
        Get value from VO which location is key

        Args:
            vo: Value Object
            key(str): location of value (ex. data.compute.instance_id)

        Returns:
            value
        """
        _LOGGER.debug(f'[_get_value_from_vo] find {key} at data')
        # Change to Dictionary
        # find at dictionary
        vot = vo.to_dict()
        key_items = key.split('.')
        if 'data' in vot:
            res = vot['data']
            for idx in key_items[1:]:
                if idx in res:
                    res = res[idx]
            return res
        _LOGGER.debug('########## NOTICE to Developer (may be Plugin Bug) #######################')
        _LOGGER.debug(f'[_get_value_from_vo] key: {key}, data: {vot}')
        _LOGGER.warning(f'[_get_value_from_vo] change_key: {key}, scope is not data')

    def _make_query_for_manager(self, key, value, filter_element):
        """
        Args:
            key(str): key for query
            value: query value of element (str, int, bool, float, list)
            filter_element(dict): one element for filter_format

        Returns:
            query_statement (list, since there are list type)

        Example)
            value: region-xxxxx
            filter_element: {'key':'region_id', 'name':'Region', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']}
        """
        query_list = []

        f_type = filter_element['type']
        if f_type == 'list':
            values = value
        else:
            values = [value]
        for val in values:
            query_list.append({'k': key, 'v': val, 'o': 'eq'})

        return query_list
