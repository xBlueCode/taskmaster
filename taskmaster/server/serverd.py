import os

from taskmaster.common import config as tm_config
from taskmaster.utils import log

from taskmaster.server.server import ServerDaemon

#data = tm_config.load("../resources/config_temp.yml")
#print(data.get('programs'))

logger_std = log.get_logger('serverd')

# server = ServerDaemon
# server = None

class ServerD():
	def __init__(self):
		self.config_server = tm_config.ConfigServer("../resources/config_temp.yml")
		self.server = ServerDaemon('/tmp/.pidfile', self.config_server)
		logger_std.info('Server Daemon has been initialized')
		logger_std.info('Starting server daemon')

	def start(self):
		logger_std.info('Starting serverd')
		self.server.start()

	def stop(self):
		logger_std.info('Stopping serverd')
		self.server.stop()


# def main():
# 	# get config file from args.
# 	# get pidfile from args.
# 	config_server = tm_config.ConfigServer("../resources/config_temp.yml")
# 	server = ServerDaemon('/tmp/.pidfile', config_server)
# 	logger_std.info('Server Daemon has been initialized')
# 	logger_std.info('Starting server daemon')
# 	server.start()


serverd = ServerD()


if __name__ == '__main__':
	log.init()
	serverd.start()
