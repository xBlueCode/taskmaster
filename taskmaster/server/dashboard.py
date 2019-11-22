from taskmaster.common.program import Program


class Dashboard:
	def __init__(self):
		self.programs = {}
		self.processes = {} # {pid: process}
		self.pid_wexit = [] # tuples returned by waitpid, (pid, exit code)
		self.pid_alive = []
		self.fds_buff = {}

	def init(self, data: dict):
		for prog in data.get('programs'):
			for prog_name, prog_data in prog.items():
				self.programs[prog_name] = prog_data




dashboard = Dashboard()
