import os, signal

from taskmaster.server.dashboard import dashboard


def sigchld_handler(signum, frame):
	if signum != signal.SIGCHLD:
		return
	# waitpid and update pid list in dashboard
	while True:
		try:
			pid_wexit = os.waitpid(0, 0)
			dashboard.pid_wexit.append(pid_wexit)
		except:
			break
