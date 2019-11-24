import signal

# from taskmaster.common.process import ProcessState, Process

import pathlib

from taskmaster.common.configmap import get_signal
from taskmaster.common.configmap import get_autorestart
from taskmaster.common.configmap import get_autostart


class Program:
    def __init__(self, name_prog, data_prog: dict):
        from taskmaster.common.process import Process
        self.name = name_prog
        self.cmd = data_prog.get('cmd')
        self.numprocs = int_def(data_prog.get('numprocs'), 0)
        self.umask = int(data_prog.get('umask'), 8)
        self.wdir = data_prog.get('wdir')
        self.delay = int_def(data_prog.get('delay'), 0)
        self.autostart = get_autostart(data_prog.get('autostart'))
        self.autorestart = get_autorestart(data_prog.get('autorestart'))
        self.exitcodes = []
        if type(data_prog.get('exitcodes')) is list:
            for code in data_prog.get('exitcodes'):
                self.exitcodes.append(int(code))
        else:
            self.exitcodes.append(int_def(data_prog.get('exitcodes'), 0))
        self.starttime = int_def(data_prog.get('starttime'), 0)
        self.stoptime = int_def(data_prog.get('stoptime'), 0)
        self.retries = int_def(data_prog.get('retries'), 0)
        self.stopsig = get_signal(data_prog.get('stopsig'), None)
        self.stddir = self.path_def(data_prog.get('stddir'))
        self.env = data_prog.get('env')
        self.processes = []
        for ind in range(self.numprocs):
            self.processes.append(
                Process(index=ind, program=self, retries=self.retries))

    def path_def(self, value, default='/tmp/tm/'):
        if isinstance(value, str):
            pathname=value
        else:
            pathname='{0}/{1}'.format(default, self.name)
        path = pathlib.Path(pathname)
        path.mkdir(parents=True, exist_ok=True)
        return path


def int_def(value, default=0):
    if value == None:
        return default
    elif isinstance(value, int):
        return value
    elif isinstance(value, str):
        return int(value)
    else:
        return default

