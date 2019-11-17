
class Program:
	def __init__(self, name_prog, data_prog:dict):
		self.name = name_prog
		self.cmd = data_prog.get('cmd')
		self.numprocs = data_prog.get('numprocs')
		self.umask = data_prog.get('umask')
		self.wdir = data_prog.get('wdir')
		self.delay = data_prog.get('delay')
		self.autostart = data_prog.get('autostart')
		self.exitcodes = []
		for code in data_prog.get('exitcodes'):
			self.exitcodes.append(int(code))
		self.starttime = data_prog.get('starttime')
		self.stoptime = data_prog.get('stoptime')
		self.retries = data_prog.get('retries')
		self.stopsig = data_prog.get('stopsig')
		self.stdin = data_prog.get('stdin')
		self.stdout = data_prog.get('stdout')
		self.stderr = data_prog.get('stderr')
		self.env = data_prog.get('env')
