# -*- coding: utf-8 -*-
import logging
import time
from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)

import random

class TestManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test(self, test):
        int = random.randrange(1, 5)
        _LOGGER.debug("---- " + test + " : sleep " + str(int) +" sec -----")
        time.sleep(int)
        _LOGGER.debug("---- " + test + " END -----")
        return test