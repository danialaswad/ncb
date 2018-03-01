import time
import unittest

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Message import Message
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class SplitterTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()

        pipeline1 = builder1.source(Timer, {"period": 1.0}).split(split_method).process(self.function1)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(1)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body)


def split_method(exchange):
    exchanges = []
    for s in exchange.in_msg.body.split():
        ex = exchange.plumber.create_exchange()
        ex.in_msg = Message()
        ex.in_msg.body = s
        exchanges.append(ex)
    return exchanges
