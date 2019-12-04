import socket

# from taskmaster.server.server import ServerDaemon
from taskmaster.utils import log
from taskmaster.utils.utils import thread_start
from taskmaster.server.service_manager import service_manager

log = log.get_logger('clients_manager')


def clients_manager(server):
    # def clients_manager(server_socket: socket.socket, config: ConfigServer):

    while True:
        cs, addr = server.socket.accept()
        thread_start(service_manager, (cs, addr, server.config))