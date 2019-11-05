import logging

EXC_INFO = False

def get_logger(name):
	if type(name) != str or name == 'config':
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s : %(levelname)-8s : %(name)-12s : %(message)s',
		)
		return logging.getLogger(name if type(name) == str else 'standard')
	else:
		logging.basicConfig(
			level= logging.INFO,
			format='%(asctime)s : %(levelname)-8s : %(name)-12s : %(message)s',
			filename= '/tmp/tm.log',
			filemode= 'w'
		)
		return logging.getLogger(name)
