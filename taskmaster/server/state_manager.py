
import os, time

from taskmaster.server.dashboard import dashboard
from taskmaster.common.state import ProcessState

from taskmaster.utils import log

logger = log.get_logger('state_handler')

def state_manager():
	# os.mkdir('/tmp/statedir')
	logger.info('starting state_handler')

	while True:
		for pid_exit in list(dashboard.pid_wexit):
			logger.info('updating state of pid: {0}'.format(pid_exit[0]))
			process = dashboard.processes.get(pid_exit[0])
			program = dashboard.programs.get(process.program_name)

			try:
				if process.state == ProcessState.RUNNING:
					process.state = ProcessState.EXITED
					logger.info('process {0} exited with code {1}'.format(pid_exit[0], pid_exit[1]))
					if pid_exit[1] in program.exitcodes:
						if program.autorestart == 'true':
							pass # launch again
					elif program.autorestart == 'unexpected':
						pass # launch again
				elif process.state == ProcessState.STOPPING:
					process.state = ProcessState.STOPPED
				elif process.state == ProcessState.BACKOFF:
					if process.retries < 1:
						process.state = ProcessState.FATAL
					else:
						process.retries = process.retries - 1
						# launch again, dec retries
			except OSError as err:
				process.state = ProcessState.UNKNOWN

			dashboard.pid_wexit.remove(pid_exit)
		time.sleep(1)