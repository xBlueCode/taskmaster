import time
import socket
import signal

from taskmaster.common.daemonizer import Daemon
from taskmaster.common.config import ConfigServer
from taskmaster.utils.sig_handler import sigchld_handler
from taskmaster.utils.utils import thread_start, socket_bind
from taskmaster.utils import log

from taskmaster.server.state_manager import state_manager
from taskmaster.server.launch_manager import launch_manager
from taskmaster.server.buff_manager import buff_manager
from taskmaster.server.service_manager import service_manager

from taskmaster.server.dashboard import dashboard

log = log.get_logger('server')


class ServerDaemon(Daemon):
    def __init__(self, pidfile, config: ConfigServer):
        super().__init__(pidfile)
        self.config = config
        self.addr = ('127.0.0.1', 4321)  # temp: to be parsed from config file
        self.socket = socket.socket()  # or in run
        self.socket_bound = False
        dashboard.init(config.data)  # change position
        signal.signal(signal.SIGCHLD, sigchld_handler)

    def run(self):
        log.info('running the server daemon')

        log.info('clients: {0}'.format(self.config.clients))
        log.info('log level {0}'.format(self.config.loglevel))

        log.info('binding the server socket')
        self.socket_bound = socket_bind(self.addr[0], self.addr[1])

        log.info('starting thread: state_handler')
        thread_start(state_manager, ())  # not none
        # thread	-> buff_handler
        log.info('starting thread: buff_manager')
        thread_start(buff_manager, ())  # not none

        # thread	-> launch_handler
        log.info('starting thread: launch_manager')
        thread_start(launch_manager, ())  # not none

        log.info('starting thread: service_manager')
        thread_start(service_manager, ())

        time.sleep(20)
        log.info('Server Daemon run ends !')

