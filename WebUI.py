from aiohttp import web
from jinja2 import Template
from threading import Thread

import asyncio

class WebUI():
    def __init__(self, host, port, rotator):
        self.rotator = rotator
        self.host = host
        self.port = port

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.app = web.Application()
        self.app.router.add_get("/", self.index)
        self.app.router.add_static("/static/", path="static", name="static")
        self.handler = self.app.make_handler()
        server = loop.create_server(self.handler, host=self.host, port=self.port)
        loop.run_until_complete(server)
        loop.run_forever()

    def index(self, request):
        print("test")
        with open("index.j2") as f:
            template_text = f.read()
        t = Template(template_text)
        return web.Response(text=t.render(event_list=self.rotator.event_list), content_type="text/html")

