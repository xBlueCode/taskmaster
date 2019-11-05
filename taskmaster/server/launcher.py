from taskmaster.utils import config as tm_config
from taskmaster.utils import log

#data = tm_config.load("../resources/config_temp.yml")
#print(data.get('programs'))

logger_std = log.get_logger(None)

config_server = tm_config.ConfigServer('../resources/config_temp.ym')
if not config_server.valid:
	logger_std.fatal('Exiting upon failed config upload')
	exit(1)
