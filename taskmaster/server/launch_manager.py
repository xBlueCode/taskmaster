
from taskmaster.utils import log

logger = log.get_logger('launch_manager')

def launch_manager():
	logger.info('starting launch_manager')
	# kill old programs in reload