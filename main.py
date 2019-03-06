import logging
import argparse
from threading import Thread

from Rotator import Rotator
from WebUI import WebUI

config="data.json"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gameserver-rotator")

log.info("initialized logging")

parser = argparse.ArgumentParser(description="Gameserver Rotator")
parser.add_argument("--web_host",
        type=str,
        nargs=1,
        help="the IP the web UI is listening on, default 0.0.0.0",
        default=["0.0.0.0"])
parser.add_argument("--web_port",
        type=int,
        nargs=1,
        help="the port the web UI is listening on, default 9000",
        default=["9000"])

parser.add_argument("--config",
        type=str,
        nargs=1,
        help="the config file to be used",
        default=["data.json"])

args = parser.parse_args()

rotator = Rotator(args.config[0])
webui = WebUI(args.web_host[0], args.web_port[0], rotator)

t = Thread(target=webui.start)
t.start()

log.info("Events sheduled")
