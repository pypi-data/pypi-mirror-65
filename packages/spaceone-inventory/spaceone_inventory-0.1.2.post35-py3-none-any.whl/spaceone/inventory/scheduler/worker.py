# -*- coding: utf-8 -*-
import logging
import json
import time
import sys

from spaceone.core import config
from spaceone.core import queue
from spaceone.core.transaction import Transaction
from spaceone.core.scheduler.worker import BaseWorker

from spaceone.api.inventory.v1.collector_pb2_grpc import CollectorServicer

_LOGGER = logging.getLogger(__name__)


"""
Job Worker
"""
class JobWorker(BaseWorker):
    def __init__(self, queue):
        super().__init__(queue)
        _LOGGER.debug("[__init__] Create JobWorker: %s" % self._name_)
        _LOGGER.debug("[__init__] Queue name: %s" % self.queue)

    def run(self):

        while True:
            # Read from queue
            # Queue format: Job Request
            sched_job = queue.get(self.queue)
            sched_job = json.loads(sched_job.decode())
            _LOGGER.debug(sched_job)

            metadata = sched_job.get('metadata', {})
            #metadata = self._fix_metadata(metadata)
            _LOGGER.debug(f'[run] metadata:{metadata}')

            service = self.locator.get_service(sched_job['API_CLASS'], metadata)
            method = getattr(service, sched_job['method'])
            param = sched_job['param']

            try:
                r = method(param)
                print(r)
            except Exception as e:
                _LOGGER.debug(e)
                _LOGGER.debug(f'[JobWorker] failed to run method: {method}, param: {param}, metadata: {metadata}')
 
    def _fix_metadata(self, data):
        """ Fix metadata 

        metadata has wrong transformation, since JSON does not have like
        [('token', 'abc}] --> [['token','abc']]

        So change inner list to ()
        """
        result = {}
        for [a,b] in data:
            result[a] = b
        return result
