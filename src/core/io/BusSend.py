from kombu import Connection

from src.core.Destination import Destination


class SimpleBusSend(object):

    def __init__(self, params):
        self.connection = params["connection"]
        self.queue_name = params["queue_name"]

    def send(self, message):
        with Connection(self.connection) as conn:
            with conn.SimpleQueue(self.queue_name) as queue:
                queue.put(message, serializer='json', compression='zlib')


class BusSend(Destination):

    def __init__(self, plumber, params):
        super(BusSend, self).__init__(plumber, params)
        self.connection = params["connection"]
        self.queue_name = params["queue_name"]

    def process(self, exchange):
        with Connection(self.connection) as conn:
            with conn.SimpleQueue(self.queue_name) as queue:
                queue.put(exchange.in_msg.body, serializer='json', compression='zlib')
