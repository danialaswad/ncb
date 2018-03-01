from src.core.Destination import Destination


class Log(Destination):
    def __init__(self, plumber, params):
        Destination.__init__(self, plumber, params)
        self.name = params["name"]

    def process(self, exchange):
        print("\nLog: " + self.name + "\n" + str(exchange) + "\n")