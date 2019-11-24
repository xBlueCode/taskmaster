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
                pid, fds = process.exec(program)
                dashboard.pid_procs[pid] = process
                dashboard.fds_buff.update(fds)
                logger.info('process {0} has been executed with pid={1}'.format(process.name, pid))
                for fd, file in fds.items():
                    logger.info('fd={0} file={1}'.format(fd, file))



def launch_process(program: Program, process: Process):
    logger.info('launching process: {0}'.format(process.name))

    # in_read, in_write = os.pipe()
    out_read, out_write = os.pipe()
    err_read, err_write = os.pipe()

    try:
        pid = os.fork()
    except OSError as err:
        logger.error('fork failed upon process execution')
        return # exit
    if pid > 0:
        dashboard.fds_buff[out_read]\
            = os.path.join(program.stddir, '{0}_out'.format(process.name))
        dashboard.fds_buff[err_read]\
            = os.path.join(program.stddir, '{0}_err'.format(process.name))
        os.close(out_write)
        os.close(err_write)
        if program.starttime > 0:
            process.state = ProcessState.STARTING
        else: # check to BACKOFF
            process.state = ProcessState.RUNNING
        dashboard.pid_procs[pid] = process
    elif pid == 0:
        os.close(out_read)
        os.close(err_read)
        # os.dup2(in_read, 0)
        os.dup2(out_write, sys.stdout.fileno())
        os.dup2(err_write, sys.stderr.fileno())
        # env, chdir, umask
        try:
            argv = program.cmd.split(' ')
            os.execve(argv[0], argv[1:], os.environ) # recheck !
        except OSError as err:
            sys.stderr.write('Failed to execve process: {0}'.format(process.name))
            exit(-1)
