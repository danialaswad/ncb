import time
import unittest

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class MulticastTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()

        pipeline1 = builder1.source(Timer, {"period": 1.0}).multicast({"aggregate_method": aggregate}) \
            .pipeline().process(self.function1).process(to_upper).process(self.function11).end_pipeline() \
            .pipeline().process(self.function111).end_pipeline() \
            .end_multicast().process(self.function1V)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(10)
        plumber.stop()


    def function1(self, ex):
        print(ex.in_msg.body + " P11")

    def function11(self, ex):
        print(ex.in_msg.body + " P12")

    def function111(self, ex):
        print(ex.in_msg.body + " P21")

    def function1V(self, ex):
        print(ex.in_msg.body + " Last")


def to_upper(exchange):
    exchange.in_msg.body = exchange.in_msg.body.upper()


def aggregate(old_exchange, current_exchange):
    if old_exchange is not None:
        current_exchange.in_msg.body += old_exchange.in_msg.body
    return current_exchange
