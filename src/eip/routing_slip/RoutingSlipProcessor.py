from src.core.Destination import Destination
from src.core.Processor import Processor
from src.core.Property import Property


class RoutingSlipProcessor(Processor):
    def __init__(self, routing_slip):
        Processor.__init__(self, None)
        self.routing_slip = routing_slip

    def _process(self, exchange):
        endpoints = self.routing_slip.slip(exchange)
        for destination_class, params in endpoints:
            assert issubclass(destination_class, Destination)
            destination = destination_class(self.routing_slip.plumber, params)
            destination.process(exchange)
            exchange.properties[Property.slip_endpoint] = destination_class
        if self.next is not None:
            self.next.process(exchange)