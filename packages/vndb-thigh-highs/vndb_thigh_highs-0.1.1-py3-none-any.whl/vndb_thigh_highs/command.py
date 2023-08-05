from abc import ABCMeta, abstractmethod
from .error import ThrottledError

class Command(metaclass=ABCMeta):
    def __init__(self, socket, response_parser):
        self.socket = socket
        self.response_parser = response_parser
        self.logger = socket.logger

    def communicate(self, command):
        while True:
            response =  self.socket.communicate(command)
            try:
                return self.response_parser.parse(response)
            except ThrottledError as throttled_error:
                self.logger.warning(
                    "Waiting because of %s" % str(throttled_error))
                throttled_error.wait_full()
                self.logger.warning("Resuming after throttled")

class ConnectCommand(Command):
    def is_connected(self):
        return self.socket.is_connected()

    def connect(self):
        self.socket.connect()

    def disconnect(self):
        self.socket.disconnect()

class TableCommand(Command):
    def __init__(self, socket, response_parser, table):
        super().__init__(socket, response_parser)
        self.table = table

    def get_name(self):
        return self.table.table_name

    def get_snakecase_name(self):
        return self.table.table_name.replace('-', '_')
