
import socket
import signal

from taskmaster.common.daemonizer import Daemon
from taskmaster.common.config import ConfigServer
from taskmaster.utils.sig_handler import sigchld_handler

class ServerDaemon(Daemon):
	def __init__(self, pidfile, config: ConfigServer):
		super().__init__(pidfile)
		self.config = config
		self.socket = socket.socket() # or in run
		signal.signal(signal.SIGCHLD, sigchld_handler)


	def run(self):
		print('do something !')
		# thread	-> state_handler
		# thread	-> buff_handler
		# thread	-> launch_handler
		# loop		-> connect:
		# 			thread	-> authenticate & serve
		print('do nothing !')