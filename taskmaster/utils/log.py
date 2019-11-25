import logging

EXC_INFO = False

filename = '/tmp/tm.log'

logging.basicConfig(
	level= logging.DEBUG,
	format='%(asctime)s : %(levelname)-8s : %(name)-16s : %(message)s',
	filename= filename,
	filemode= 'w'
)


def get_logger(name = 'standard'):
	return logging.getLogger(name)
