import socket
import ssl
from .error import CertificateError, SocketError

class SocketConfig:
    def __init__(self):
        self.hostname = "api.vndb.org"
        self.port = 19535
        self.end_of_transmission = b"\x04"
        self.buffer_size = 4096
        self.timeout = 5

    def get_address(self):
        return self.hostname, self.port

class Socket:
    def __init__(self, logger, socket_config=None):
        self.config = socket_config or SocketConfig()
        self.logger = logger
        self.socket = None

    def connect(self):
        if self.is_connected():
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.config.timeout)
        context = ssl.create_default_context()
        self.socket = context.wrap_socket(sock, server_hostname=self.config.hostname)
        self.socket.connect(self.config.get_address())
        certificate = self.socket.getpeercert()
        if ssl.match_hostname(certificate, self.config.hostname) is not None:
            raise CertificateError("Wrong certificate!")

    def disconnect(self):
        if not self.is_connected():
            return
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.socket = None

    def is_connected(self):
        return self.socket is not None

    def communicate(self, message):
        self.send(message)
        return self.receive()

    def send(self, message):
        message = message.encode()
        message += self.config.end_of_transmission
        self.logger.info("Sending '%s'." % message)
        total = 0
        while total < len(message):
            sent = self.socket.send(message)
            if sent == 0:
                raise SocketError("Socket connection broken")
            total += sent

    def receive(self):
        chunks = []
        while True:
            chunk = self.socket.recv(self.config.buffer_size)
            self.logger.info("Receiving data...")
            if chunk.endswith(self.config.end_of_transmission):
                chunk = chunk.rstrip(self.config.end_of_transmission)
                chunks.append(chunk)
                break
            chunks.append(chunk)
        response = b"".join(chunks).decode()
        self.logger.debug("Response '%s'" % response)
        return response
