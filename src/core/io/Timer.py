import threading

import time

from src.core.Exchange import Exchange
from src.core.Message import Message
from src.core.Source import Source


class Timer(Source):
    def __init__(self, plumber, params):
        Source.__init__(self, plumber, params)
        self.period = float(params["period"])
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
        self.period = source.period
        self.plumber = plumber
        self.count = 0

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            time.sleep(self.period)
            if self.plumber is not None:
                exchange = self.plumber.create_exchange()
            else:
                exchange = Exchange()
            message = Message()
            message.body = "This is exchange " + str(self.count)
            exchange.in_msg = message
            self.source.chain.process(exchange)
            self.count += 1
