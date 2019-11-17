import yaml

from taskmaster.utils import log

logger_std = log.get_logger('config')

class Config:
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = self.load()
		if self.data is not None:
			logger_std.info('Config file has beeen loaded successfully')
			self.valid = True
		else:
			logger_std.error('Failed to load config file')
			self.valid = False
		#print(self.data)

	def load(self):
		"""\
		Loads the yaml file
		:param filepath: the path to the yaml file
		:return: configuration data from the yaml file
		"""
		data = None
		try:
			with open(self.filepath, 'r') as cfile:
				data = yaml.load(cfile, Loader=yaml.FullLoader)
				cfile.close()
		except Exception as e:
			logger_std.error('Failed to open config file', exc_info=log.EXC_INFO)
		return data

	def save(self):
		"""
		Save the provided data to a yaml file with the provide path
		:param filepath:
		:param data:
		:return: None
		"""
		with open(self.filepath, 'w') as cfile:
			yaml.dump(self.data, cfile)


class ConfigServer(Config):
	def __init__(self, filepath):
		super().__init__(filepath)
		if not self.valid:
			logger_std.error('failed to create a valid Server Config')
			return
		self.x = 5


def load(filepath):
	"""\
	Loads the yaml file
	:param filepath: the path to the yaml file
	:return: configuration data from the yaml file
	"""
	data = None
	try:
		with open(filepath, 'r') as cfile:
			data = yaml.load(cfile, Loader = yaml.FullLoader)
			cfile.close()
	except Exception as e:
		logger_std.error('Failed to open config file', exc_info=log.EXC_INFO)
	return data

def save(filepath, data):
	"""
	Save the provided data to a yaml file with the provide path
	:param filepath:
	:param data:
	:return: None
	"""
	with open(filepath, 'w') as cfile:
		yaml.dump(data, cfile)
