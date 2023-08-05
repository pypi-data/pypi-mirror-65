import logging
from .login_command import LoginConfig

class Config:
    def __init__(self):
        self.name = "VNDB Thigh-highs"
        self.log_level = logging.WARNING
        self.logger = self.create_logger(self.name)
        self.login = LoginConfig(self.name)

    def create_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(self.log_level)
            logger.addHandler(handler)
        return logger

    def set_login(self, username, password):
        self.login.set_login(username, password)

    def set_log_level(self, log_level):
        self.log_level = log_level
        self.logger.setLevel(self.log_level)
