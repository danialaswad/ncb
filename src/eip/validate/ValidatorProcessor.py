from src.core.Processor import Processor


class ValidatorProcessor(Processor):

    def __init__(self, validator):
        Processor.__init__(self, None)
        self.validator = validator

    def _process(self, exchange):
        result = self.validator.validate(exchange)
        if result:
            if self.next is not None:
                self.next.process(exchange)
        else:
            raise ValueError("Exchange failed validation")
