from src.core.Channel import Channel
from src.core.Destination import Destination
from src.core.Processor import Processor
from src.core.Status import Status
from src.eip.agregator.Aggregator import Aggregator
from src.eip.agregator.AggregatorPocess import AggregatorProcessor
from src.eip.cbr.ContentBasedRouter import ContentBasedRouter
from src.eip.cbr.ContentBasedRouterProcessor import ContentBasedRouterProcessor
from src.eip.dynamic_router.DynamicRouter import DynamicRouter
from src.eip.dynamic_router.DynamicRouterProcessor import DynamicRouterProcessor
from src.eip.filter.Filter import Filter
from src.eip.filter.FilterProcessor import FilterProcessor
from src.eip.multicast.Multicast import Multicast
from src.eip.multicast.MulticastProcessor import MulticastProcessor
from src.eip.resequencer.Resequencer import Resequencer
from src.eip.resequencer.ResequencerProcessor import ResequencerProcessor
from src.eip.routing_slip.RoutingSlip import RoutingSlip
from src.eip.routing_slip.RoutingSlipProcessor import RoutingSlipProcessor
from src.eip.split.Splitter import Splitter
from src.eip.split.SplitterProcessor import SplitterProcessor
from src.eip.validate.Validator import Validator
from src.eip.validate.ValidatorProcessor import ValidatorProcessor
from src.eip.wiretap.Wiretap import Wiretap


class Pipeline(object):
    def __init__(self, builder, plumber):
        self.id = builder.id
        self.plumber = plumber
        self.status = Status.stopped
        self.auto_start = builder.auto_start
        self.source = builder.source_class(plumber, builder.source_params)
        self.transient_previous = None
        self.wiretap = None
        for destination in builder.to_list:
            if destination[0] == Wiretap:
                self.wiretap = destination[1]
                continue
            channel = Channel(self.plumber, {"wiretap": self.wiretap})
            if self.source.chain is None:
                self.source.chain = channel
            if issubclass(destination[0], Destination):
                destination_obj = destination[0](plumber, destination[1])
                processor = Processor(destination_obj)
            if issubclass(destination[0], Splitter):
                destination_obj = destination[0](plumber)
                processor = SplitterProcessor(destination_obj)
            if issubclass(destination[0], Filter):
                destination_obj = destination[0](plumber)
                processor = FilterProcessor(destination_obj)
            if issubclass(destination[0], Aggregator):
                destination_obj = destination[0](plumber, destination[1])
                processor = AggregatorProcessor(destination_obj)
            if issubclass(destination[0], RoutingSlip):
                destination_obj = destination[0](plumber, destination[1])
                processor = RoutingSlipProcessor(destination_obj)
            if issubclass(destination[0], DynamicRouter):
                destination_obj = destination[0](plumber, destination[1])
                processor = DynamicRouterProcessor(destination_obj)
            if issubclass(destination[0], Validator):
                destination_obj = destination[0](plumber)
                processor = ValidatorProcessor(destination_obj)
            if destination[0] == Multicast:
                destination_obj = destination[0](plumber, destination[1])
                processor = MulticastProcessor(destination_obj)
            if destination[0] == ContentBasedRouter:
                destination_obj = destination[0](plumber, destination[1])
                processor = ContentBasedRouterProcessor(destination_obj)
            if destination[0] == Resequencer:
                destination_obj = destination[0](plumber, destination[1])
                processor = ResequencerProcessor(destination_obj)
            channel.next = processor
            if self.transient_previous is not None:
                self.transient_previous.next = channel
            self.transient_previous = processor
            self.wiretap = None

    def start(self):
        self.status = Status.starting
        self.source.start()
        self.status = Status.running

    def stop(self):
        self.status = Status.stopping
        self.source.stop()
        self.status = Status.stopped
