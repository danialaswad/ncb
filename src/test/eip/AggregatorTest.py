import unittest

import time

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class AggregatorTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()
        pipeline1 = builder1.source(Timer, {"period": 1.0}).aggregate({"method": aggregate, "count": 5, "timeout": 2}).process(self.function1)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(12)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body)


def aggregate(old_exchange, current_exchange):
    if old_exchange is not None:
        current_exchange.in_msg.body += old_exchange.in_msg.body
    return current_exchange
