import requests
import json

from src.core.Destination import Destination
from src.core.RouteBuilder import RouteBuilder
from src.core.io.BusReceive import BusReceive, SimpleBusReceive
from src.core.io.BusSend import BusSend, SimpleBusSend

connection = 'zookeeper://guest:guest@localhost:4041//'


class SimpleRoute(RouteBuilder):
    def __init__(self):
        super(SimpleRoute, self).__init__()
        self.from_ = SimpleBusSend({"connection": connection, "queue_name": "test1"})
        self.to_ = SimpleBusReceive({"connection": connection, "queue_name": "test2"})

    def build(self):
        self.pipeline = self.builder.source(BusReceive, {"connection": connection, "queue_name": "test1"}) \
            .to(MessageModifier)\
            .to(BusSend, {"connection": connection, "queue_name": "test2"}).build()
        self.pipeline.start()

    def input(self, message):
        self.from_.send(message)

    def output(self):
        return self.to_.receive()


class MessageModifier(Destination):
    def process(self, exchange):
        r = requests.post('http://httpbin.org/post', data={'name': 'danial aswad'})
        exchange.in_msg.body = json.loads(r.text)
