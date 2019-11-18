import time

from taskmaster.common.state import ProcessState

class Process:
	def __init__(self, pid, program = None, state = None, status = ProcessState.STOPPED,
				 retries = 0, fds = None):
		self.pid = pid
		self.program = program
		self.state = state
		self.status = status
		self.retries = retries
		self.ctime = time.time() # creation time
		self.dtime = None # death time
		self.fds = fds[:]
