import os

from taskmaster.common import config as tm_config
from taskmaster.utils import log

from taskmaster.server.server import ServerDaemon

#data = tm_config.load("../resources/config_temp.yml")
#print(data.get('programs'))

logger_std = log.get_logger('serverd')

def main():
	logger_std.info('Starting serverd')
	# get config file from args.
	# get pidfile from args.
	config_server = tm_config.ConfigServer("../resources/config_temp.yml")
	server = ServerDaemon('/tmp/.pidfile', config_server)
	logger_std.info('Server Daemon has been initialized')
	logger_std.info('Starting server daemon')
	server.start()

if __name__ == '__main__':
	log.init()
	main()


