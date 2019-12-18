import os, time, sys, signal, pathlib

from taskmaster.common.configmap import ProcessState
from taskmaster.common.program import Program

from taskmaster.utils.utils import thread_start


class Process:
    """\
    Process object contains all necessary information about:
    the name of the parent program and the index of the process in the list.
    pid, state, status, timestamps, and current retries number.
    file descriptors linked to the std_out and std_err
    """
    def __init__(self, index=0, program:Program=None, status=None, state=ProcessState.CREATED,
                 retries=0, fds=None):
        # from taskmaster.common.program import Program
        self.index = index
        self.pid = -1
        self.state = state
        self.status = status
        self.ctime = time.time()  # creation time
        self.stime = None # start time
        self.dtime = None  # death time
        if not program or not isinstance(program, Program):
            return
        self.program_name = program.name
        self.name = '{0}_{1:03d}'.format(program.name, index)
        self.retries = program.retries
        self.fds = []
        self.to_remove = False

    def exec(self, program):
        """
        Here's the magic of fork/exec.
        It creates two pipes and link them to the std_out/std_err of the process
        After fork, the parent process will return the pid of the child process
        and the list of the file descriptors linked to the standard out/err of child process.
        :param program:
        :return:
        """
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
            fds = {}  # {fd: file}
            fds[out_read] = pathlib.Path(program.stddir / '{0}_out'.format(self.name))
            fds[err_read] = pathlib.Path(program.stddir / '{0}_err'.format(self.name))
            self.fds.append(out_read)
            self.fds.append(err_read)
            os.close(out_write)
            os.close(err_write)
            self.stime = time.time()
            self.dtime = None
            thread_start(self.starting_state_tracker, (program,))
            return pid, fds
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
                os.execve(argv[0], argv, os.environ)  # recheck !
                exit(1)
            except OSError as err:
                exit(-1)

    def starting_state_tracker(self, program: Program):  # must be used in a thread
        """\
        It decides about the state of the process upon starting depending on the staring time
        if the starting time is 0, then it sets the state directly to RUNNING,
        otherwise, it waits* until the end of the starting time then it sets
        the process's state to RUNNING if it sill in the STARTING state.

        * This is a blocking method so it must be executed in its own thread.
        :param program:
        :return:
        """
        if program.starttime > 0:
            self.state = ProcessState.STARTING
            time.sleep(program.starttime)
            if self.state == ProcessState.STARTING:
                self.state = ProcessState.RUNNING
        else:  # check to BACKOFF
            self.state = ProcessState.RUNNING

    def control_starting_state(self, program: Program):
        """\
        It decides about the state of the process when it is exited while
        it's in the starting/backoff state.
        :param program:
        :return:
        """
        if self.state != ProcessState.STARTING \
                and self.state != ProcessState.BACKOFF:
            return
        time_diff = time.time() - self.stime
        if time_diff >= program.starttime: # this is additional to ss_tracker in case of race condition
            self.state = ProcessState.RUNNING
        else:
            self.state = ProcessState.BACKOFF

    def kill(self, stopsig=signal.SIGKILL):
        if self.state != ProcessState.STARTING \
                and self.state != ProcessState.BACKOFF \
                and self.state != ProcessState.RUNNING:
            return 1
        self.state = ProcessState.STOPPING
        try:
            os.kill(self.pid, signal.SIGKILL)  # get signal from data
            return 0
        except OSError:
            return 1
