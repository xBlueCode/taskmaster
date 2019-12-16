import os, signal

from taskmaster.server.dashboard import dashboard

from taskmaster.utils import log

log = log.get_logger('sig_handler')


def sigchld_handler(signum, frame):
    if signum != signal.SIGCHLD:
        return
    # waitpid and update pid list in dashboard
    while True:
        try:
            pid_wexit = os.waitpid(0, 0)
            dashboard.pid_wexit.append(pid_wexit)
        except OSError as err:
            log.fatal('error occurred upon waiting pid')
            exit(1)
