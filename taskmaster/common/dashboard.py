
from taskmaster.common.program import Program

class Dashboard:
	def __init__(self, data: dict):
		self.programs = []
		for name_prog, data_prog in data.get('programs').items():
			self.programs.append(Program(name_prog, data_prog))
		self.processes = {} # {pid: process}
		self.pid_signaled = []
		self.pid_alive = []





dashboard = None



def init(data: dict):
	global dashboard
	dashboard = Dashboard(data)