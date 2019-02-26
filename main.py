import json
import datetime
import logging

from Event import Event

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gameserver-rotator")

log.info("initialized logging")

def json_event_parser(d):
    return { k : v if k not in ["start_time", "stop_time"] else datetime.datetime.fromisoformat(v) for k,v in d.items()}

with open("data.json") as f:
    input_list = json.load(f, object_hook=json_event_parser)

log.info("data.json loaded")

event_list = list()
for event in input_list:
    event_list.append(Event(**event))

log.info("Events sheduled")
