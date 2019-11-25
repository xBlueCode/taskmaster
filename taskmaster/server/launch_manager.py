import os, sys

from taskmaster.common.process import Process, ProcessState

from taskmaster.common.program import Program

from taskmaster.utils import log
from taskmaster.server.dashboard import dashboard

from taskmaster.common import configmap

logger = log.get_logger('launch_manager')


def launch_manager():
    logger.info('starting launch_manager')
    # kill old programs in reload or create reload_manager
    logger.info('debug: fds_buff: {0}'.format(dashboard.fds_buff.keys()))
    for prog_name, program in dashboard.programs.items():
        # logger.info('launching program {0} -> numprocs={1}'.format(prog_name, program.numprocs))
        logger.info('launching program {0}, umask={1}'.format(prog_name, program.umask))
        logger.info('launching {0}'.format(program.cmd.split(' ')))
        for process in program.processes:
            dashboard.name_procs[process.name] = process # move to higher level
            if program.autostart == configmap.Start.NO:
                process.state = ProcessState.STOPPED
            else:
                launch_process(program, process)


def launch_process(program: Program, process: Process):
    logger.info('launching process: {0}'.format(process.name))
    pid, fds = process.exec(program)
    dashboard.pid_procs[pid] = process
    dashboard.fds_buff.update(fds)
    logger.info('process {0} has been executed with pid={1}'.format(process.name, pid))
    for fd, file in fds.items():
        logger.info('fd={0} file={1}'.format(fd, file))
