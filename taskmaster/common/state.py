from enum import Enum, auto


class ProcessState(Enum):
	STOPPED = auto()
	STARTING = auto()
	RUNNING = auto()
	BACKOFF = auto()
	STOPPING = auto()
	EXITED = auto()
	FATAL = auto()
	UNKNOWN = auto()




STOPPED_STATES = (ProcessState.STOPPED,
                  ProcessState.EXITED,
                  ProcessState.FATAL,
                  ProcessState.UNKNOWN)




RUNNING_STATES = (ProcessState.RUNNING,
                  ProcessState.BACKOFF,
                  ProcessState.STARTING)
