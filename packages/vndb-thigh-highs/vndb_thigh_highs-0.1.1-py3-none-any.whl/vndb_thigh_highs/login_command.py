import json
from .command import ConnectCommand
from .response_parser import OkResponseParser

class LoginConfig:
    def __init__(self, client_name):
        self.protocol = 1
        self.client_name = client_name
        self.client_version = 0.1
        self.username = None
        self.password = None

    def set_login(self, username, password):
        self.username = username
        self.password = password

    def make_login_dict(self):
        args = {
            'protocol': self.protocol,
            'client': self.client_name,
            'clientver': self.client_version,
        }
        if self.username is not None and self.password is not None:
            args['username'] = self.username
            args['password'] = self.password
        return args

class LoginCommand(ConnectCommand):
    def __init__(self, socket, login_config):
        super().__init__(socket, OkResponseParser.for_login())
        self.config = login_config
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def login(self):
        if not self.is_connected():
            self.connect()
        command = self.make_command()
        self.communicate(command)
        self.logged_in = True

    def logout(self):
        self.logged_in = False
        self.disconnect()

    def make_command(self):
        login_dict = self.config.make_login_dict()
        command = "login %s" % json.dumps(login_dict)
        return command
