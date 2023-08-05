# -*- coding: utf-8 -*-

import multiprocessing
import logging
from spaceone.core import config
from spaceone.core.error import *

#from spaceone.core.scheduler import BaseScheduler

_LOGGER = logging.getLogger(__name__)


class Server(object):
    def __init__(self, service, config):
        self.service = service
        self.config = config
        self.queues = {}
        self.schedulers = {}
        self.workers = {}

    def start(self):
     
        ###################
        # Queues
        ###################
        if 'QUEUES' not in self.config:
            _LOGGER.error('QUEUES is not configured')
            # TODO: exit
        # Load Queue config
        self.queues = self.config['QUEUES']

        ####################
        # Start Schedulers
        ####################
        if 'SCHEDULERS' not in self.config:
            _LOGGER.warn('SCHEDULERS is not configured')
            _LOGGER.warn('Scheduling will be triggered remotely')
            self.config['SCHEDULERS'] = {}

        for (name, conf) in self.config['SCHEDULERS'].items():
            params = conf.copy()
            if 'backend' not in conf:
                _LOGGER.debug('Backend is not specified')
                # TODO: ERROR
            backend = conf['backend']
            del params['backend']
            if 'queue' not in conf:
                _LOGGER.debug('Queue is not specified')
                # TODO: ERROR
            self.schedulers[name] = self._create_process(backend, params) 

        #######################
        # Start Workers
        #######################
        if 'WORKERS' not in self.config:
            _LOGGER.warn('WORKER is not configured')
            _LOGGER.warn('May be schduler only')
            self.config['WORKERS'] = {}
            # TODO: exit
        # Load Worker config
        for (name, conf) in self.config['WORKERS'].items():
            params = conf.copy()
            if 'backend' not in conf:
                _LOGGER.debug('Backend is not specified')
                # TODO: ERROR
            backend = conf['backend']
            del params['backend']
            if 'queue' not in conf:
                _LOGGER.debug('Queue is not specified')
                # TODO: ERROR
            # self.queue is instance of Queue
            self.workers[name] = self._create_process(backend, params) 


        # Start All threads
        # start worker
        for (k,v) in self.workers.items():
            v.start()

        # start scheduler
        for (k,v) in self.schedulers.items():
            v.start()

    def _create_process(self, backend, params):
        # create scheduler
        _LOGGER.debug(params)
        try:
            module_name, class_name = backend.rsplit('.', 1)
            scheduler_module = __import__(module_name, fromlist=[class_name])
            return getattr(scheduler_module, class_name)(**params)
        except ERROR_BASE as error:
            # TODO:
            raise err
        except Exception as e:
            # TODO
            raise e

def serve():
    # Load scheduler config
    # Create Scheduler threads
    # start Scheduler
    conf = config.get_global()
    server = Server(config.get_service(), conf)
    server.start()
