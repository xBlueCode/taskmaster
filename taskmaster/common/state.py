
class ProcessState:
	STOPPED = 0
	STARTING = 1
	RUNNING = 2
	BACKOFF = 3
	STOPPING = 4
	EXITED = 5
	FATAL = 6
	UNKNOWN = 7

STOPPED_STATES = (ProcessState.STOPPED,
                  ProcessState.EXITED,
                  ProcessState.FATAL,
                  ProcessState.UNKNOWN)

RUNNING_STATES = (ProcessState.RUNNING,
                  ProcessState.BACKOFF,
                  ProcessState.STARTING)
