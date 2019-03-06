import logging
import json
import datetime

from Event import Event
from threading import RLock

log = logging.getLogger("gameserver-rotator")

class Rotator():
    def __init__(self, config=None):
        """parses the given config file and creates the Events.
        The event_list is empty if config=None"""

        def json_event_parser(d):
            """ parses the JSON Objects and converts the dates to datetime objects"""
            return { k : v if k not in ["start_time", "stop_time"] else\
                    datetime.datetime.fromisoformat(v) for k,v in d.items()}

        input_list = list()
        if config is not None:
            with open(config,"r") as f:
                input_list = json.load(f, object_hook=json_event_parser)

        log.info("config %s loaded" % config)

        self.event_list = [Event(**e) for e in input_list]
        self.event_lock = RLock()

