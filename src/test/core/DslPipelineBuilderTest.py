import inspect
import unittest

from src.core.Destination import Destination
from src.core.DslPipelineBuilder import DslPipelineBuilder
from src.core.Source import Source


class DslPipelineDefinitionBuilderTest(unittest.TestCase):

    def test_simple_pipeline(self):
        builder = DslPipelineBuilder()
        builder.source(Source1).to(To1).to(To2)
        self.assertEqual(builder.source_class, Source1)

    def test_process_block(self):
        builder = DslPipelineBuilder()

        def function1(x):
            print(x)

        builder.source(Source1).to(To1).to(To2).process(function1)
        self.assertEqual(builder.source_class, Source1)
        self.assertTrue(inspect.isclass(builder.to_list[2][0]))

    def test_one_source(self):
        builder = DslPipelineBuilder()
        with self.assertRaises(AssertionError):
            builder.to(To1)

    def test_only_one_source(self):
        builder = DslPipelineBuilder()
        with self.assertRaises(AssertionError):
            builder.source(To1).source(To1)

    def test_build_pipeline(self):
        builder = DslPipelineBuilder()
        pipeline = builder.source(Source1).to(To1).to(To2).build()
        self.assertIsNotNone(pipeline.source.chain)

    def test_multicast_dsl(self):
        builder = DslPipelineBuilder()
        builder.source(Source1).to(To1).multicast({})\
            .pipeline().to(To1).to(To1).end_pipeline()\
            .pipeline().to(To1).to(To1).end_pipeline()\
            .end_multicast().to(To1)
        self.assertIsNotNone(builder._builder_stack[-1])


class Source1(Source):
    def stop(self):
        pass

    def start(self):
        pass


class To1(Destination):
    def process(self, exchange):
        pass


class To2(Destination):
    def process(self, exchange):
        pass


if __name__ == '__main__':
    unittest.main()