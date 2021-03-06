import time
import unittest

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class ValidatorTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()

        pipeline1 = builder1.source(Timer, {"period": 1.0}).validate(Filter()).process(self.function1)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(2)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body)


class Filter:
    def __call__(self, exchange):
        parts = exchange.in_msg.body.split()
        return int(parts[-1]) % 2 == 0


def filter_method(exchange):
    parts = exchange.in_msg.body.split()
    return int(parts[-1]) % 2 == 0
