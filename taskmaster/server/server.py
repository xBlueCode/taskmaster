
import time
import socket
import signal

from taskmaster.common.daemonizer import Daemon
from taskmaster.common.config import ConfigServer
from taskmaster.utils.sig_handler import sigchld_handler
from taskmaster.utils.threading import thread_start
from taskmaster.utils import log

from taskmaster.server.state_manager import state_manager
from taskmaster.server.launch_manager import launch_manager
from taskmaster.server.buff_manager import buff_manager

from taskmaster.server.dashboard import dashboard

logger = log.get_logger('server')

class ServerDaemon(Daemon):
	def __init__(self, pidfile, config: ConfigServer):
		super().__init__(pidfile)
		self.config = config
		self.socket = socket.socket() # or in run
		dashboard.init(config.data) # change position
		signal.signal(signal.SIGCHLD, sigchld_handler)

	def run(self):
		logger.info('running the server daemon')
		logger.info('starting thread: state_handler')
		# thread_start(state_manager, ()) # not none

		# thread	-> buff_handler
		logger.info('starting thread: buff_handler')
		# thread_start(buff_manager, ()) # not none

		# thread	-> launch_handler
		logger.info('starting thread: launch_handler')
		thread_start(launch_manager, ()) # not none

		# loop		-> connect:
		# 			thread	-> authenticate & serve
		print('do nothing !')
		time.sleep(20)
		logger.info('Server Daemon run ends !')
