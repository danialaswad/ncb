import time
import unittest

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Timer import Timer


class ContentBasedRouterTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()
        pipeline1 = builder1.source(Timer, {"period": 1.0}).content_based_router() \
            .when(lambda ex: int(ex.in_msg.body.split()[-1]) % 3 == 0).pipeline().process(self.function1).end_pipeline() \
            .when(lambda ex: int(ex.in_msg.body.split()[-1]) % 3 == 1).pipeline().process(self.function11).end_pipeline() \
            .otherwise().pipeline().process(self.function111).end_pipeline() \
            .end_content_based_router().process(self.function1V)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(10)
        plumber.stop()

    def function1(self, ex):
        print(ex.in_msg.body + " %0")

    def function11(self, ex):
        print(ex.in_msg.body + " %1")
    def function111(self, ex):
        print(ex.in_msg.body + "  Otherwise")

    def function1V(self, ex):
        print(ex.in_msg.body + " Last")


