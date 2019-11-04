import yaml
import logging

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

logger_std = get_logger('config')

class Config:
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = load(filepath)
		logger_std.info('Config file has beeen loaded successfully')
		print(self.data)


def load(filepath):
	"""\
	Loads the yaml file
	:param filepath: the path to the yaml file
	:return: configuration data from the yaml file
	"""
	with open(filepath, 'r') as cfile:
		return yaml.load(cfile, Loader = yaml.FullLoader)


def save(filepath, data):
	"""
	Save the provided data to a yaml file with the provide path
	:param filepath:
	:param data:
	:return: None
	"""
	with open(filepath, 'w') as cfile:
		yaml.dump(data, cfile)

