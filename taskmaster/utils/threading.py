import threading

from taskmaster.utils import log

logger = log.get_logger('threading')

def thread_start(target, args):
	logger.info('creating thread')
	thread = threading.Thread(target=target, args=args)
	logger.info('starting thread')
	thread.start()