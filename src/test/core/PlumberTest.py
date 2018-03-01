import unittest

import time

from src.core.Destination import Destination
from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class PlumberTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()
        builder2 = DslPipelineBuilder()
        pipeline1 = builder1.source(Timer, {"period": 1.0}).to(MessageModifier).process(self.function1)
        pipeline2 = builder2.source(Timer, {"period": 2.0}).to(MessageModifier).process(self.function11)
        plumber.add_pipeline(pipeline1)
        plumber.add_pipeline(pipeline2)
        plumber.start()
        time.sleep(10)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body + " Pipeline1")
        return ex

    def function11(self, ex):
        print(ex.in_msg.body + " Pipeline2")
        return ex


class MessageModifier(Destination):
    def process(self, exchange):
        exchange.in_msg.body += " modified"
