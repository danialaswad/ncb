import time
import unittest

from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Plumber import Plumber
from src.core.io.Log import Log
from src.core.io.Timer import Timer


class WiretapTest(unittest.TestCase):

    def test_wiretap(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(Timer, {"period": 1.0}).wiretap((Log, {"name": "wiretap"})).to(Log, {"name": "actual"})
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(1)
        plumber.stop()
