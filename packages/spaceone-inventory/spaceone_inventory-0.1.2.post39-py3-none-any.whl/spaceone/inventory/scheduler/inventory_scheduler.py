# -*- coding: utf-8 -*-
import consul
import datetime
import logging
import json
import time
import sys

from spaceone.core import config
from spaceone.core import queue
from spaceone.core.locator import Locator
from spaceone.core.scheduler import HourlyScheduler

_LOGGER = logging.getLogger(__name__)

"""
Inventory Hourly Scheduler
"""

def _get_domain_id_from_token(token):
    decoded_token = JWTUtil.unverified_decode(token)
    return decoded_token['did']

WAIT_QUEUE_INITIALIZED = 10     # seconds for waiting queue initilization
INTERVAL = 10
MAX_COUNT = 10

def _validate_token(token):
    if isinstance(token, dict):
        protocol = token['protocol']
        if protocol == 'consul':
            consul_instance = Consul(token['config'])
            value = False
            count = 0
            while value is False:
                uri = token['uri']
                value = consul_instance.patch_token(uri)
                _LOGGER.warn(f'[_validate_token] token: {value} uri: {uri}')
                if value:
                    break
                time.sleep(INTERVAL)

            token = value 

    _LOGGER.debug(f'[_validate_token] token: {token}')
    return token

class InventoryHourlyScheduler(HourlyScheduler):
    def __init__(self, queue, interval, minute=':00'):
        super().__init__(queue, interval, minute)
        self.count = self._init_count()
        self.locator = Locator()
        self.TOKEN = self._update_token()

    def _init_count(self):
        # get current time
        cur = datetime.datetime.now()
        count = {
            'previous': cur,            # Last check_count time
            'index' : 0,                # index
            'hour': cur.hour,           # previous hour
            'started_at': 0,            # start time of push_token
            'ended_at': 0               # end time of execution in this tick
            }
        _LOGGER.debug(f'[_init_count] {count}')
        return count

    def _update_token(self):
        token = config.get_global('TOKEN')
        if token == "":
            token = _validate_token(config.get_global('TOKEN_INFO'))
        return token

    def push_token(self):
        try:
            ok = self.check_count()
            if ok == False:
                # ERROR LOGGING
                pass
            # Loop all domain, then find scheduled collector
            collector_svc = self.locator.get_service('CollectorService')
            schedule = {'hour': self.count['hour']}
            _LOGGER.debug(f'[push_token] schedule: {schedule}')
            scheduler_vos, total = collector_svc.scheduled_collectors({'schedule':schedule})
            _LOGGER.debug(f'[push_token] scheduled count: {total}')
            _LOGGER.debug(f'[push_token] scheduler_vo: {scheduler_vos}')
            for scheduler_vo in scheduler_vos:
                # Create Job Request
                jobs  = self._create_job_request(scheduler_vo)
                # Push Job at Queue
                for job in jobs:
                    _LOGGER.debug(f'[push_token] {job}')
                    json_job = json.dumps(job)
                    queue.put(self.queue, json_job)

            # update count['ended_at']
            #self._update_count_ended_at()
        except Exception as e:
            _LOGGER.error(e)
            print("pass failed")

    def check_count(self):
        # check current count is correct or not
        cur = datetime.datetime.now()
        hour = cur.hour
        # check
        if (self.count['hour'] + self.config) % 24 != hour:
            if self.count['hour'] == hour:
                _LOGGER.error('[check_count] duplicated call in the same time')
            else:
                _LOGGER.error('[check_count] missing time')

        # This is continuous task
        count = {
            'previous': cur,
            'index': self.count['index'] + 1,
            'hour': hour,
            'started_at': cur
            }
        self.count.update(count)

    def _update_count_ended_at(self):
        cur = datetime.datetime.now()
        self.count['ended_at'] = cur

    def _create_job_request(self, scheduler_vo):
        """ Based on scheduler_vo, create Job Request

        Args:
            scheduler_vo: Scheduler VO
                - scheduler_id
                - name
                - collector: Reference of Collector
                - schedule
                - filter
                - collector_mode
                - created_at
                - last_scheduled_at
                - domain_id
                }
        
        Returns:
            jobs: list

        Because if collector_info has credential_group_id,
        we have to iterate all credentials in the credential_group
        """
        _LOGGER.debug(f'[_create_job_request] scheduler_vo: {scheduler_vo}')
        _LOGGER.debug(f'plugin_info1: {scheduler_vo.collector}') 
        _LOGGER.debug(f'plugin_info2: {scheduler_vo.collector.plugin_info}') 
        _LOGGER.debug(f'plugin_info3: {scheduler_vo.collector.plugin_info.plugin_id}') 
        plugin_info = scheduler_vo.collector.plugin_info
        _LOGGER.debug(f'plugin_info: {plugin_info}') 
        domain_id = scheduler_vo.domain_id
        credential_list = []

        _LOGGER.debug(f'credential_list: {credential_list}')
        if plugin_info.credential_id:
            _LOGGER.debug(f'[_create_job_request] Add Credential: {plugin_info.credential_id}')
            credential_list.append(plugin_info.credential_id)

        if plugin_info.credential_group_id:
            _LOGGER.debug(f'[_create_job_request] Add Credential Group: {plugin_info.credential_group_id}')
            collector_svc = self.locator.get_service('CollectorService', metadata={'token': self.TOKEN})
            params = {'credential_group_id': plugin_info.credential_group_id, 'domain_id': domain_id}
            creds_list = collector_svc.get_credentials_by_grp_id(params)
            credential_list.extend(creds_list)

        jobs = []
        _LOGGER.debug(f'credential_list: {credential_list}')
        for credential_id in credential_list:
            sched_job = {
                'API_CLASS': 'CollectorService',
                'method': 'collect',
                'param': {
                    'collector_id': scheduler_vo.collector.collector_id,
                    # if filter
                    # contact credential
                    'credential_id': credential_id,
                    'collect_mode': 'ALL',
                    'filter': {},
                    'domain_id': domain_id
                    },
                'metadata': {
                    'token': self.TOKEN,
                    'domain_id': domain_id
                    }
            }
            _LOGGER.debug(f'[_create_job_request] sched_job: {sched_job}')
            jobs.append(sched_job)

        return jobs

class Consul:
    def __init__(self, config):
        """
        Args:
          - config: connection parameter

        Example:
            config = {
                    'host': 'consul.example.com',
                    'port': 8500
                }
        """
        self.config = self._validate_config(config)

    def _validate_config(self, config):
        """
        Parameter for Consul
        - host, port=8500, token=None, scheme=http, consistency=default, dc=None, verify=True, cert=None
        """
        options = ['host', 'port', 'token', 'scheme', 'consistency', 'dc', 'verify', 'cert']
        result = {}
        for item in options:
            value = config.get(item, None)
            if value:
              result[item] = value
        return result

    def patch_token(self, key):
        """
        Args:
            key: Query key (ex. /debug/supervisor/TOKEN)

        """
        try:
            conn = consul.Consul(**self.config)
            index, data = conn.kv.get(key)
            return data['Value'].decode('ascii')

        except Exception as e:
            return False


