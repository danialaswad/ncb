import threading

from kombu import Connection

from src.core.Exchange import Exchange
from src.core.Message import Message
from src.core.Source import Source


class SimpleBusReceive(object):

    def __init__(self, params):
        self.connection = params["connection"]
        self.queue_name = params["queue_name"]

    def receive(self):
        with Connection(self.connection) as conn:
            with conn.SimpleQueue(self.queue_name) as queue:
                message = queue.get(block=True, timeout=10)
                message.ack()
                in_message = message.payload
        return in_message


class BusReceive(Source):

    def __init__(self, plumber, params):
        super(BusReceive, self).__init__(plumber, params)
        self.connection = params["connection"]
        self.queue_name = params["queue_name"]
        self.thread = None

    def start(self):
        self.thread = TimerThread(self, self.plumber)
        self.thread.start()

    def stop(self):
        self.thread.stop()


class TimerThread(threading.Thread):
    def __init__(self, source, plumber):
        threading.Thread.__init__(self)
        self.stopped = False
        self.source = source
        self.connection = source.connection
        self.queue_name = source.queue_name
        self.plumber = plumber
        self.count = 0

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            with Connection(self.connection) as conn:
                with conn.SimpleQueue(self.queue_name) as queue:
                    message = queue.get(block=True, timeout=10)
                    message.ack()
                    in_message = message.payload
            if self.plumber is not None:
                exchange = self.plumber.create_exchange()
            else:
                exchange = Exchange()
            message = Message()
            message.body = in_message
            exchange.in_msg = message
            self.source.chain.process(exchange)
            self.stop()
