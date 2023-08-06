# -*- coding: utf-8 -*-
import json
import logging

from spaceone.core import queue

from spaceone.core.scheduler.worker import BaseWorker

_LOGGER = logging.getLogger(__name__)

"""
Service Worker
"""

class ServiceWorker(BaseWorker):
    def __init__(self, queue):
        super().__init__(queue)
        _LOGGER.debug(f'[__init__] Create ServiceWorker: name: {self.name}, queue: {self.queue}')

    def run(self):
        while True:
            # Read from queue
            # Queue format: Service Request format
            queue_job = queue.get(self.queue)

            # Parse Job
            try:
                json_job = json.loads(queue_job.decode())
                metadata = json_job.get('metadata', {})
            except Exception as e:
                _LOGGER.error(e)
                _LOGGER.debug(f'[run] Fail to decode JSON job: {queue_job}')

            # Get Service
            try:
                service = self.locator.get_service(json_job['API_CLASS'], metadata)
                method = getattr(service, json_job['method'])
                param = json_job['param']
            except Exception as e:
                _LOGGER.error(e)
                _LOGGER.debug(f'[run] Fail to get Service: {json_job}')

            # Run method
            try:
                r = method(param)
                _LOGGER.debug(f'[run] result: {r}')
            except Exception as e:
                _LOGGER.error(e)
                _LOGGER.debug(f'[run] Fail to run method: {method}, param: {param}, metadata: {metadata}')

