import os, time, sys

from taskmaster.common.configmap import ProcessState
from taskmaster.common.program import Program


class Process:
    def __init__(self, index=0, program:Program=None, status=None, state=ProcessState.CREATED,
                 retries=0, fds=None):
        # from taskmaster.common.program import Program
        self.index = index
        self.pid = -1
        self.state = state
        self.status = status
        self.ctime = time.time()  # creation time
        self.dtime = None  # death time
        self.fds = []
        if not program or not isinstance(program, Program):
            return
        self.program_name = program.name
        self.name = '{0}_{1:03d}'.format(program.name, index)
        self.retries = program.retries
        self.fds = []

    def exec(self, program):
        # in_read, in_write = os.pipe()
        out_read, out_write = os.pipe()
        err_read, err_write = os.pipe()

        try:
            pid = os.fork()
        except OSError as err:
            # logger.error('fork failed upon process execution')
            return # exit
        if pid > 0:
            self.pid = pid
            fds = {}
            fds[out_read] = program.stddir / '{0}_out'.format(self.name)
            fds[err_read] = program.stddir / '{0}_err'.format(self.name)
            self.fds.append(out_read)
            self.fds.append(err_read)
            os.close(out_write)
            os.close(err_write)
            if program.starttime > 0:
                self.state = ProcessState.STARTING
            else: # check to BACKOFF
                self.state = ProcessState.RUNNING
            # dashboard.processes[pid] = process
            return (pid, fds)
        elif pid == 0:
            os.close(out_read)
            os.close(err_read)
            # os.dup2(in_read, 0)
            os.dup2(out_write, sys.stdout.fileno())
            os.dup2(err_write, sys.stderr.fileno())
            os.close(out_write)
            os.close(err_write)
            # env, chdir, umask
            program.config_process()
            try:
                argv = program.cmd.split(' ')
                os.execve(argv[0], argv, os.environ) # recheck !
                exit(1)
            except OSError as err:
                # sys.stderr.write('Failed to execve process: {0}'.format(process.name))
                exit(-1)
