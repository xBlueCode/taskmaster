import os, time
from select import select


from taskmaster.utils import log

from taskmaster.server.dashboard import dashboard

logger = log.get_logger('buff_handler')

def buff_manager():
	logger.info('starting buff_handler')

	while True:
		time.sleep(1)
		if len(dashboard.fds_buff):
			continue
		try:
			rfds, wfds, xfds = select(dashboard.fds_buff, [], [])
		except OSError:
			logger.error('error occurred upon select fds')
			continue
		for fd in rfds:
			data = os.read(fd, 1024)
			if not data:
				continue
			filename = dashboard.fds_buff.get(fd)
			if not filename:
				continue
			with open(filename, os.O_CREAT | os.O_WRONLY | os.O_APPEND) as file:
				file.write(data)
