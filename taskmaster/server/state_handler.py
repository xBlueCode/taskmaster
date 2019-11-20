
import os

from taskmaster.utils import log

logger = log.get_logger('state_handler')

def state_handler():
	# os.mkdir('/tmp/statedir')
	logger.info('starting state_handler')