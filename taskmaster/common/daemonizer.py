"""Linux daemon base class for python3.x"""

import sys, os, time, atexit, signal, errno




class Daemon:
	"""\
	Generic daemon class"""
	def __init__(self, pidfile):
		self.pidfile = pidfile


	def daemonize(self):
		"""Daemonise mechanism"""

		try:
			# first fork
			pid = os.fork()
			if pid > 0: #exit first parent
				sys.exit(0)
		except OSError as err:
			sys.stderr.write('first fork failed: {0}\n'.format(err))
			sys.exit(1)

		# decouple from parent environment
		os.chdir('/')
		os.setsid()
		os.umask(0)

		# second fork
		try:
			pid = os.fork()
			if pid > 0:  # exit second parent
				sys.exit(0)
		except OSError as err:
			sys.stderr.write('second fork failed: {0}\n'.format(err))
			sys.exit(1)

		pid = os.getpid()
		try:
			with open(self.pidfile, 'w+') as file:
				file.write(str(pid) + '\n')
		except PermissionError as err:
			sys.stderr.write('error: failed to open pidfile, errno = {0}\n'.format(err.errno))
			sys.stderr.write('exiting with 1')
			exit(1)
		self.pid = pid

		# direct standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		stdi = open(os.devnull, 'r')
		stdo = open(os.devnull, 'a+')
		stde = open(os.devnull, 'a+')

		os.dup2(stdi.fileno(), sys.stdin.fileno())
		os.dup2(stdo.fileno(), sys.stdout.fileno())
		os.dup2(stde.fileno(), sys.stderr.fileno())

		# write pidfile
		atexit.register(self.delpid)



	def	delpid(self):
		try:
			os.remove(self.pidfile)
		except OSError as err:
			sys.stderr.write('Failed to remove pidfile: {0}'.format(err))


	def start(self):
		"""Start the daemon"""
		# checking if the daemon is already running
		try:
			with open(self.pidfile, 'r') as pfile:
				pid = int(pfile.read().strip())
		except IOError as err:
			pid = None
			# sys.stderr.write('Failed to read from pidfile, pid var got None value')
		if pid:
			msg = "pidfile {0} already exist"
			sys.stderr.write(msg.format(self.pidfile))
			sys.exit(1)
		# start the daemon
		print('daemonizing !')
		self.daemonize()
		print('daemonized !')
		self.run()


	def stop(self):
		"Stop the daemon"
		try:
			with open(self.pidfile, 'r') as pfile:
				pid = int(pfile.read().strip())
		except IOError as err:
			pid = None
		if not pid:
			msg = "pidfile {0} does't exist"
			sys.stderr.write(msg.format(self.pidfile))
			return
		try:
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			if err.errno == errno.ESRCH:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				sys.stderr.write("Failed to kill the process {0}".format(pid))
				sys.exit(1)


	def restart(self):
		"""Restart the daemon"""
		self.stop()
		self.start()


	def	run(self):
		"To be implemented in the subclass"
		pass
