import os, sys, time, signal

from taskmaster.common.process import Process, ProcessState

from taskmaster.common.program import Program

from taskmaster.utils import log
from taskmaster.utils import utils
from taskmaster.server.dashboard import dashboard

from taskmaster.common import configmap

log = log.get_logger('launch_manager')


def launch_manager():
    """
    Launches all programs in the list contained in the dashboard
    :return:
    """
    log.info('starting launch_manager')
    # kill old programs in reload or create reload_manager
    log.info('debug: fds_buff: {0}'.format(dashboard.fds_buff.keys()))
    for program in dashboard.programs.values():
        launch_program(program)


def reload_launch_manager(new_programs: {str: Program}):
    log.info('starting reload launch manager')
    old_programs = dashboard.programs
    nprog_names = list(new_programs.keys())
    oprog_names = list(old_programs.keys())
    for oprog_name, oprog in old_programs.items():
        if oprog_name not in nprog_names:
            dashboard.prog_to_remove.append(oprog_name)

def launch_program(program: Program, force_start=False):
    """
    Launches a program by launching all the processes created by this program
    if the start is forced by client or autostart is enabled then
    Otherwise, all processes will be moved to STOPPED state.
    :param program: Program object to be launched.
    :param force_start: True if client requesting a start.
    :return:
    """
    if not program or not isinstance(program, Program):
        return
    log.info('launching program {0}, umask={1}'.format(program.name, program.umask))
    log.info('launching {0}'.format(program.cmd.split(' ')))
    for process in program.processes:
        log.debug('Starting new process !')
        # dashboard.name_procs[process.name] = process # move to higher level
        log.debug('AUTO_START -------- {} === {}'.format(program.autostart, configmap.Start.NO))
        if program.autostart is False:
            process.state = ProcessState.STOPPED
        else:
            launch_process(program, process)

        # if force_start == True or program.autostart != configmap.Start.No:
        #     launch_process(program, process)
        # else:
        #     log.debug('moving it to stopped !')
        #     process.state = ProcessState.STOPPED


def launch_process(program: Program, process: Process, retry:bool = False):
    """
    Launches a process and update the dashboard by the pid of the launched process
    and the opened file descriptors.
    :param program: Parent program of the process.
    :param process: The process to be launched.
    :param retry: True if the process is being restarted from a retry
    :return:
    """
    log.info('launching process: {0}'.format(process.name))
    if retry:
        process.retries = process.retries - 1
        if process.retries < 1:
            return
    while process.state == ProcessState.STOPPING:  # recheck
        time.sleep(1)
    pid, fds = process.exec(program)
    dashboard.pid_procs[pid] = process
    dashboard.fds_buff.update(fds)
    log.info('process {0} has been executed with pid={1}'.format(process.name, pid))
    for fd, file in fds.items():
        log.info('fd={0} file={1}'.format(fd, file))
    dashboard.name_procs[process.name] = process # move to higher level


def kill_process(process: Process, stopsig=signal.SIGKILL):
    log.debug('killing process {0}'.format(process.name))
    if process.state != ProcessState.STARTING \
            and process.state != ProcessState.BACKOFF \
            and process.state != ProcessState.RUNNING:
        return 1
    process.state = ProcessState.STOPPING
    try:
        os.kill(process.pid, stopsig)  # get signal from data
        log.debug('killing signal has been sent to {0}'.format(process.pid))
    except OSError:
        log.error('failed to kill process {0}:[{1}]'.format(process.name, process.pid))


def kill_program(program: Program):
    for process in program.processes:
        utils.thread_start(kill_process, (process, program.stopsig))