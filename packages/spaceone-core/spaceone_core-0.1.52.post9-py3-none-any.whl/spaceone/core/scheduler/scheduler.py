# -*- coding: utf-8 -*-

import schedule
import sys
import time
import logging
from multiprocessing import Process
from spaceone.core import queue

_LOGGER = logging.getLogger(__name__)

class BaseScheduler(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.config = None
        self.upper_count = 0
        self.count = 0
        self._intmax = sys.maxsize

    def push_token(self):

        if self.count >= self._intmax:
            self.upper_count = self.upper_count + 1
            self.count = 0

        self.count = self.count + 1
        _LOGGER.debug("Push token at %s" % self.queue)
        queue.put(self.queue, self.count)

    def run(self):
        NotImplementedError('scheduler.run is not implemented')

class IntervalScheduler(BaseScheduler):
    def __init__(self, queue, interval):
        super().__init__(queue)
        self.config = self.parse_config(interval)

    def parse_config(self, expr):
        """ expr
          format: integer (second)
        """
        try:
            if type(expr) == type(1):
                return int(expr)
        except Exception as e:
            _LOGGER.error('Wrong configraiton')

    def run(self):

        schedule.every(self.config).seconds.do(self.push_token)
        while True:
            schedule.run_pending()
            time.sleep(1)

"""
HourlyScheduler starts every HH:00
If you want to start at different minutes
send minute like ':15' meaning every 15 minute
"""
class HourlyScheduler(BaseScheduler):
    def __init__(self, queue, interval=1, minute=':00'):
        super().__init__(queue)
        self.config = self.parse_config(interval)
        self.minute = minute

    def parse_config(self, expr):
        """ expr
          format: integer (hour)
        """
        try:
            if type(expr) == type(1):
                return int(expr)
        except Exception as e:
            _LOGGER.error('Wrong configuration')
            raise ERROR_CONFIGURATION(key='interval')

    def run(self):
        # Call push_token in every hour
        schedule.every(self.config).hour.at(self.minute).do(self.push_token)
        while True:
            schedule.run_pending()
            time.sleep(1)


"""
cronjob: min hour day month week
"""
class CronScheduler(BaseScheduler):

    def __init__(self, queue):
        super().__init__(queue, rule)
        self.config = self.parse_config(rule)

    def parse_config(self, config):
        """ expr
          format: min hour day month week
          * * * * *
        """
        items = expr.split(' ')
        if len(items) != 5:
            return False
        # TODO: verify format
        return items

    def run(self):
        if self.config == False:
            # May be error format
            return

        # Minute
        if self.config[0] == '*':
            schedule.every().minutes.do(self.push_token)
        else:
            schedule.every(int(self.config[0])).minutes.do(self.push_token)
       
        # Hour
        if self.config[1] == '*':
            schedule.every().hour.do(self.push_token)
        else:
            schedule.every(int(self.config[1])).hour.do(self.push_token)

        # Day
        if self.config[2] == '*':
            schedule.every().day.do(self.push_token)
        else:
            schedule.every(int(self.config[2])).day.do(self.push_token)

        # Month
        if self.config[3] != '*':
            _LOGGER.warn("Month is not applicable")

        while True:
            schedule.run_pending()
            time.sleep(1)
