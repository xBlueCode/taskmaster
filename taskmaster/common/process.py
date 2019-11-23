import time

from taskmaster.common.configmap import ProcessState


class Process:
    def __init__(self, index=0, program=None, status=None, state=ProcessState.CREATED,
                 retries=0, fds=None):
        self.index = index
        self.pid = -1
        self.program_name = program
        self.name = '{0}_{1:03d}'.format(program, index)
        self.state = state
        self.status = status
        self.retries = retries
        self.ctime = time.time()  # creation time
        self.dtime = None  # death time
        self.fds = []
        # self.fds = fds[:]
