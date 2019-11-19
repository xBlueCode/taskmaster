
import socket
import signal

from taskmaster.common.daemonizer import Daemon
from taskmaster.common.config import ConfigServer
from taskmaster.utils.sig_handler import sigchld_handler
from taskmaster.utils.threading import thread_start

from .buff_handler import buff_handler
from .launch_handler import launch_handler
from .state_handler import state_handler

class ServerDaemon(Daemon):
	def __init__(self, pidfile, config: ConfigServer):
		super().__init__(pidfile)
		self.config = config
		self.socket = socket.socket() # or in run
		signal.signal(signal.SIGCHLD, sigchld_handler)

	def run(self):
		print('do something !')
		# thread	-> state_handler
		thread_start(state_handler, None) # not none

		# thread	-> buff_handler
		thread_start(buff_handler, None) # not none

		# thread	-> launch_handler
		thread_start(launch_handler, None) # not none

		# loop		-> connect:
		# 			thread	-> authenticate & serve
		print('do nothing !')