import unittest

import time

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Log import Log
from src.core.io.Timer import Timer


class LogTest(unittest.TestCase):

    def test_log(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(Timer, {"period": 1.0}).to(Log, {"name": "test"})
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(1)
        plumber.stop()
