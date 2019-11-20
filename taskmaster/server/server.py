
import os
import socket
import signal
import threading

from taskmaster.common.daemonizer import Daemon
from taskmaster.common.config import ConfigServer
from taskmaster.utils.sig_handler import sigchld_handler
from taskmaster.utils.threading import thread_start
from taskmaster.utils import log

from taskmaster.server.state_handler import state_handler
from taskmaster.server.launch_handler import launch_handler
from taskmaster.server.buff_handler import buff_handler

logger = log.get_logger('server')

class ServerDaemon(Daemon):
	def __init__(self, pidfile, config: ConfigServer):
		super().__init__(pidfile)
		self.config = config
		self.socket = socket.socket() # or in run
		signal.signal(signal.SIGCHLD, sigchld_handler)

	def run(self):
		logger.info('running the server daemon')
		logger.info('starting thread: state_handler')
		thread_start(state_handler, ()) # not none

		# thread	-> buff_handler
		logger.info('starting thread: buff_handler')
		thread_start(buff_handler, ()) # not none

		# thread	-> launch_handler
		logger.info('starting thread: launch_handler')
		thread_start(launch_handler, ()) # not none

		# loop		-> connect:
		# 			thread	-> authenticate & serve
		print('do nothing !')
