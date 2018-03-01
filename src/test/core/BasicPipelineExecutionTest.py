import unittest

import time

from src.core.Destination import Destination
from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.io.Timer import Timer


def process(ex):
    print(ex.in_msg.body)


class BasicPipelineExecutionTest(unittest.TestCase):

    def test_simple_pipeline(self):
        builder = DslPipelineBuilder()
        pipeline = builder.source(Timer, {"period": 1.0}).to(MessageModifier).process(
            process).build()
        pipeline.start()
        time.sleep(10)
        pipeline.stop()


class MessageModifier(Destination):
    def process(self, exchange):
        exchange.in_msg.body += " modified"
