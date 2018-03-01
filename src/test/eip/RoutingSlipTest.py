import time
import unittest

from src.core.Destination import Destination
from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class FilterTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()

        pipeline1 = builder1.source(Timer, {"period": 1.0}).routing_slip({"method": slip}).process(self.function1)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(1)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body)


def slip(exchange):
    return [
        (D1, {}),
        (D2, {})
    ]


class D1(Destination):
    def process(self, exchange):
        print(exchange.in_msg.body + " D1")


class D2(Destination):
    def process(self, exchange):
        print(exchange.in_msg.body + " D2")
