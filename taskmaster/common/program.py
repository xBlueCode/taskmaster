
import signal

class Program:
	def __init__(self, name_prog, data_prog:dict):
		self.name = name_prog
		self.cmd = data_prog.get('cmd')
		# self.numprocs = data_prog.get('numprocs')
		self.numprocs = int_def(data_prog.get('numprocs'), 0)
		self.umask = data_prog.get('umask')
		self.wdir = data_prog.get('wdir')
		self.delay = int_def(data_prog.get('delay'), 0)
		self.autostart = data_prog.get('autostart')
		self.exitcodes = []
		if type(data_prog.get('exitcodes')) is list:
			for code in data_prog.get('exitcodes'):
				self.exitcodes.append(int(code))
		else:
			self.exitcodes.append(int_def(data_prog.get('exitcodes'), 0))
		self.starttime = int_def(data_prog.get('starttime'), 0)
		self.stoptime = int_def(data_prog.get('stoptime'), 0)
		self.retries = int_def(data_prog.get('retries'), 0)
		self.stopsig = data_prog.get('stopsig')
		self.stddir = data_prog.get('stddir')
		self.env = data_prog.get('env')




def int_def(value, default = 0):
	if not value or not isinstance(value, str):
		return default
	else:
		return int(value)
