from src.core.Processor import Processor


class ContentBasedRouterProcessor(Processor):
    def __init__(self, cbr):
        Processor.__init__(self, None)
        self.cbr = cbr

    def _process(self, exchange):
        pipeline = self.cbr.get_valid_pipeline(exchange)
        if pipeline is not None:
            pipeline.source.chain.process(exchange)
            if self.next is not None:
                self.next.process(exchange)
