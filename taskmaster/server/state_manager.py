import os, time

from taskmaster.server.dashboard import dashboard
from taskmaster.common.configmap import ProcessState
from taskmaster.common.process import Process

from taskmaster.utils import log

logger = log.get_logger('state_manager')


def state_manager():
    # os.mkdir('/tmp/statedir')
    logger.info('starting state_manager')

    while True:
        logger.info('checking processes state')
        for pid_exit in list(dashboard.pid_wexit):
            logger.info('updating state of pid: {0}'.format(pid_exit[0]))
            process = dashboard.pid_procs.get(pid_exit[0])
            program = dashboard.programs.get(process.program_name)

            try:
                if process.state == ProcessState.RUNNING:
                    process.state = ProcessState.EXITED
                    logger.info('process {0} exited with code {1}'.format(pid_exit[0], pid_exit[1]))
                    clean_proccess(process)
                    logger.info('process {0} has been cleaned'.format(pid_exit[0]))
                    if pid_exit[1] in program.exitcodes:
                        if program.autorestart == 'true':
                            pass  # launch again
                    elif program.autorestart == 'unexpected':
                        pass  # launch again
                elif process.state == ProcessState.STOPPING:
                    process.state = ProcessState.STOPPED
                elif process.state == ProcessState.BACKOFF:
                    if process.retries < 1:
                        process.state = ProcessState.FATAL
                    else:
                        process.retries = process.retries - 1
                    # launch again, dec retries
            except OSError as err:
                process.state = ProcessState.UNKNOWN

            dashboard.pid_wexit.remove(pid_exit)
        time.sleep(1)


def clean_proccess(process:Process):
    process.dtime = time.time()
    dashboard.pid_procs.pop(process.pid)
    process.pid = -1
    logger.debug('cleaning process fds: {0}'.format(process.fds))
    for fd in process.fds:
        try:
            # os.close(fd)
            process.fds.remove(fd)
            dashboard.fds_zombie.append(fd)
            # dashboard.fds_buff.pop(fd)
        except OSError as err:
            logger.error('failed to close fd={0}'.format(fd))
    logger.debug('fds_zombies: {0}'.format(dashboard.fds_zombie))
    # process.fds.clear()
    # add fds to old list
