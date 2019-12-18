import signal

from enum import Enum, auto


class ProcessState(Enum):
    CREATED = auto()
    STOPPED = auto()
    STARTING = auto()
    RUNNING = auto()
    BACKOFF = auto()
    STOPPING = auto()
    EXITED = auto()
    FATAL = auto()
    REMOVED = auto()
    UNKNOWN = auto()


class Start(Enum):
    YES = auto()
    NO = auto()

class Restart(Enum):
    ALWAYS = auto()
    NEVER = auto()
    UNEXPECTED = auto()


AUTO_START = {
    'yes':          Start.YES,
    'no':           Start.NO,
}


AUTO_RESTART = {
    'always': Restart.ALWAYS,
    'never': Restart.NEVER,
    'unexpected': Restart.UNEXPECTED
}


STOPPED_STATES = (ProcessState.STOPPED,
                  ProcessState.EXITED,
                  ProcessState.FATAL,
                  ProcessState.UNKNOWN)


RUNNING_STATES = (ProcessState.RUNNING,
                  ProcessState.BACKOFF,
                  ProcessState.STARTING)


SIGNALS = {
    'term': signal.SIGTERM,
    'int':  signal.SIGINT,
    'hup':  signal.SIGHUP,
    'quit': signal.SIGQUIT,
    'kill': signal.SIGKILL,
    'usr1': signal.SIGUSR1,
    'usr2': signal.SIGUSR2
}


def get_signal(signame: str, default = signal.SIGKILL):
    sig = SIGNALS.get(signame.lower())
    if sig:
        return sig
    else:
        return default


def get_autostart(name:str, default=Start.NO):
    if name is None:
        return default
    if isinstance(name, bool):
        return name
    elif isinstance(name, str):
        autostart = AUTO_START.get(name.lower())
        if autostart != None:
            return autostart
        else:
            return default


def get_autorestart(name:str, default=Restart.NEVER):
    if name is None:
        return default
    elif isinstance(name, str):
        autorestart = AUTO_RESTART.get(name.lower())
        if autorestart:
            return autorestart
        else:
            return default
    else:
        return default
