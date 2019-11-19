import signal


def sigchld_handler(signum, frame):
	if signum != signal.SIGCHLD:
		return
	# waitpid and update pid list in dashboard
