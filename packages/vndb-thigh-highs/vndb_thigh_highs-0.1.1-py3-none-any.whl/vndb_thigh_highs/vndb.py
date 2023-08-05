from functools import wraps
from .socket import Socket
from .config import Config
from .login_command import LoginCommand
from .dbstats_command import DBStatsCommand
from .get_command import GetCommandFactory
from .set_command import SetCommandFactory

def auto_login(login_command):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not login_command.is_logged_in():
                login_command.login()
            return function(*args, **kwargs)
        return decorated_function
    return decorator

class VNDB:
    def __init__(self, *, config=None, socket=None):
        self.config = config or Config()
        self.socket = socket or Socket(self.config.logger)
        self._init_commands()

    def _init_commands(self):
        self._init_login_logout_commands()
        self._init_dbstats_command()
        self._init_get_commands()
        self._init_set_commands()

    def _init_login_logout_commands(self):
        self.login_command = LoginCommand(self.socket, self.config.login)
        self.login = self.login_command.login
        self.logout = self.login_command.logout
        self.login_decorator = auto_login(self.login_command)

    def _init_dbstats_command(self):
        dbstats_command = DBStatsCommand(self.socket)
        self._add_method("dbstats", dbstats_command.get)

    def _add_method(self, name, method):
        method = self.login_decorator(method)
        method.__name__ = name
        setattr(self, name, method)

    def _init_get_commands(self):
        factory = GetCommandFactory(self.socket)
        for get_command in factory.all_commands():
            get_method_name = "get_%s" % get_command.get_snakecase_name()
            self._add_method(get_method_name, get_command.get)
            get_all_method_name = "get_all_%s" % get_command.get_snakecase_name()
            self._add_method(get_all_method_name, get_command.get_all)

    def _init_set_commands(self):
        factory = SetCommandFactory(self.socket)
        for set_command in factory.all_commands():
            set_method_name = "set_%s" % set_command.get_snakecase_name()
            self._add_method(set_method_name, set_command.set)
            delete_method_name = "delete_%s" % set_command.get_snakecase_name()
            self._add_method(delete_method_name, set_command.delete)
