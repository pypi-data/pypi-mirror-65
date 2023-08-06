# -*- coding: utf-8 -*-
import logging
from threading import Timer as _Timer

logger = logging.getLogger('vindauga.types.timer')


class Timer:
    """
    Basic timers to handle things like waiting for Escape keys
    """
    def __init__(self):
        self._timer = None
        self._running = False
        self._expired = True

    def start(self, timeout):
        if self._timer:
            self._timer.cancel()
        self._timer = _Timer(timeout, self.expire)
        self._timer.start()
        self._running = True
        self._expired = False

    def stop(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._running = False
        self._expired = True

    def expire(self):
        self._expired = True

    def isRunning(self):
        return self._running

    def isExpired(self):
        return self._expired
