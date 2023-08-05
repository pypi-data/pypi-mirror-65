# -*- coding: utf-8 -*-

import random
import string
import time
import logging

from multiprocessing import Process

from spaceone.core import config
from spaceone.core.locator import Locator


_LOGGER = logging.getLogger(__name__)


def randomString(stringLength=8):
    """Generate a random string of fixed length """
    letters= string.ascii_lowercase
    return ''.join(random.sample(letters,stringLength))

class BaseWorker(Process):
    locator = Locator()

    def __init__(self, queue):
        super().__init__()
        self._name_ = 'worker-%s' % randomString()
        self.queue = queue

    def run(self):
        pass

