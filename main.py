import logging
from threading import Thread

from Rotator import Rotator
from WebUI import WebUI

config="data.json"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gameserver-rotator")

log.info("initialized logging")

rotator = Rotator(config)
webui = WebUI("localhost", 9000, rotator)

t = Thread(target=webui.start)
t.start()

log.info("Events sheduled")
