from src.core.DslPipelineBuilder import DslPipelineBuilder


class RouteBuilder(object):
    def __init__(self):
        self.builder = DslPipelineBuilder()
        self.pipeline = None
        self.to_ = None
        self.from_ = None

    def build(self):
        raise NotImplementedError("Subclass of destination needs to implement process method")

    def input(self, message):
        raise NotImplementedError("Subclass of destination needs to implement process method")

    def output(self):
        raise NotImplementedError("Subclass of destination needs to implement process method")
