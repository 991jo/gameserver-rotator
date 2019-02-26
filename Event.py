from datetime import datetime, timedelta
from threading import Timer

import subprocess
import shlex

import logging

log = logging.getLogger("gameserver-rotator")

class Event():

    def __init__(self, start_time, stop_time, start_script, stop_script, name, description):
        """ creates a new event."""
        self._start_time = start_time
        self._stop_time = stop_time
        self._start_script = start_script
        self._stop_script = stop_script
        self.name = name
        self.description = description
        self.running = False

        # default initialization with a Timer that does nothing
        self._start_timer = Timer(0,lambda : 0)
        self._stop_timer = Timer(0,lambda : 0)

        self._set_start_timer()
        self._set_stop_timer()

    def __repr__(self):
        return "< Event '%s' from %s to %s with scripts '%s' and '%s' >" % \
            (
                self.name,
                self.start_time.isoformat(),
                self.stop_time.isoformat(),
                self.start_script,
                self.stop_script
            )

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """ set the start time of the Event and enables the timer."""

        self._start_time = value
        self._set_start_timer()

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, value):
        """ set the stop time of the Event and enables the timer."""

        self._stop_time = value
        self._set_stop_timer()

    @property
    def start_script(self):
        return self._start_script

    @start_script.setter
    def start_script(self, value):
        """ set the start_script of the Event and enables the timer"""

        self._start_script = value
        self._set_start_timer()

    @property
    def stop_script(self):
        return self._stop_script

    @stop_script.setter
    def stop_script(self, value):
        """ set the stop_script of the Event and enables the timer"""

        self._stop_script = value
        self._set_stop_timer()

    def start(self):
        """ executes the start script, aborts the start timer if running."""
        log.info("starting %s" % self.name)
        result = self._execute_script(self.start_script)
        self.running = True
        log.info("started %s" % self.name)
        log.info(result)

    def stop(self):
        """ executes the stop script, aborts the stop timer if running."""
        log.info("stoping %s" % self.name)
        result = self._execute_script(self.stop_script)
        self.running = False
        log.info("stopped %s" % self.name)
        log.info(result)

    def _execute_script(self, script):
        """ executes a script using subprocess ans shlex."""
        command = shlex.split(script)
        return subprocess.run(command, shell=True)


    def cancel_start(self):
        """ cancels the start timer if running."""

        if self._start_timer is not None:
            self._start_timer.cancel()
            self._start_timer = None
            log.info("canceled start timer for %s" % self.name)

    def cancel_stop(self):
        """ cancels the stop timer if running."""

        if self._stop_timer is not None:
            self._stop_timer.cancel()
            self._stop_timer = None
            log.info("canceled stop timer for %s" % self.name)


    def enable_start(self):
        """ enables the start timer if it is not running."""

        self._set_start_timer()

    def enable_stop(self):
        """ enables the stop timer if it is not running."""

        self._set_stop_timer()

    def _set_start_timer(self):
        """ sets the start timer if it is in the future and cancels the old one
        if it is running. """

        if self.start_time is None:
            return

        self.cancel_start()

        seconds_to_start = (self.start_time - datetime.now()).total_seconds()
        if seconds_to_start > 0:
            self._start_timer = Timer(seconds_to_start, self.start)
            self._start_timer.start()
            log.info("set start timer for %s" % self.name)


    def _set_stop_timer(self):
        """ sets the stop timer if it is in the future and cancels the old one
        if it is running. """

        if self.start_time is None:
            return

        self.cancel_stop()

        seconds_to_stop = (self.stop_time - datetime.now()).total_seconds()
        if seconds_to_stop > 0:
            self._stop_timer = Timer(seconds_to_stop, self.stop)
            self._stop_timer.start()
            log.info("set stop timer for %s" % self.name)
