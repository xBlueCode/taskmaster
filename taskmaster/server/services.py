import os, time

from taskmaster.utils import log

from taskmaster.utils import utils
from taskmaster.common.configmap import ProcessState
from taskmaster.common import config as tm_config

from taskmaster.server import dashboard as mod_dash
from taskmaster.server.dashboard import dashboard

from taskmaster.server.launch_manager import launch_process
from taskmaster.server.launch_manager import reload_launch_manager
from taskmaster.server.launch_manager import kill_process
from taskmaster.server.launch_manager import kill_program

log = log.get_logger('services')


def serve_start(cs, query_list):
    log.info('serving: start: {0}'.format(query_list))
    # utils.socket_send(cs, 'something there from start')
    # utils.socket_send(cs, '\r')
    prog_names = query_list[1:]
    log.debug('prog_names: {0}'.format(prog_names))
    for prog_name in prog_names:
        if prog_name not in dashboard.programs.keys():
            utils.socket_send(cs, 'program {0} not found'.format(prog_name))
        else:
            utils.socket_send(cs, 'starting {0}'.format(prog_name))
            program = dashboard.programs.get(prog_name)
            changed = 0
            for process in program.processes:
                utils.socket_send(cs, 'process {0} is in {1} state'
                                  .format(process.name, process.state))
                if process.state != ProcessState.STARTING \
                        and process.state != ProcessState.BACKOFF \
                        and process.state != ProcessState.RUNNING:
                    # see if it needs to reset retries
                    utils.socket_send(cs, 'starting process: {0}'.format(process.name))
                    launch_process(program, process)


def serve_restart(cs, query_list):
    log.info('serving: restart: {0}'.format(query_list))
    prog_names = query_list[1:]
    for prog_name in prog_names:
        if prog_name not in dashboard.programs.keys():
            utils.socket_send(cs, 'program {0} not found'.format(prog_name))
        else:
            utils.socket_send(cs, 'restarting {0}'.format(prog_name))
            program = dashboard.programs.get(prog_name)
            for process in program.process:
                utils.socket_send(cs, 'process {0} is in {1} state'.
                                  format(process.name, process.state))
                if process.state == ProcessState.STARTING \
                        or process.state == ProcessState.BACKOFF \
                        or process.state == ProcessState.RUNNING:
                    utils.socket_send(cs, 'stopping process {0}'.format(process.name))
                    #kill process
                    utils.thread_start(kill_process, (process, program.stopsig))
                    utils.socket_send(cs, 'starting process: {0}'.format(process.name))
                    launch_process(program, process)


def serve_stop(cs, query_list):
    log.info('serving: stop: {0}'.format(query_list))
    prog_names = query_list[1:]
    stop_programs(cs, prog_names)


def stop_programs(cs, prog_names):
    for prog_name in prog_names:
        if prog_name not in dashboard.programs.keys():
            utils.socket_send(cs, 'program {0} not found'.format(prog_name))
        else:
            utils.socket_send(cs, 'stopping {0}'.format(prog_name))
            program = dashboard.programs.get(prog_name)
            for process in program.processes:
                utils.socket_send(cs, 'process {0} is in {1} state'.
                                  format(process.name, process.state))
                if process.state == ProcessState.STARTING \
                        or process.state == ProcessState.BACKOFF \
                        or process.state == ProcessState.RUNNING:
                    utils.socket_send(cs, 'stopping process {0}'.format(process.name))
                    # kill process
                    utils.thread_start(kill_process, (process, program.stopsig))



def serve_relaod(cs, query_list):
    log.info('serving: reload: {0}'.format(query_list))
    if len(query_list) < 2:
        utils.socket_send(cs, 'err: config file is required')
        return
    config_server = tm_config.ConfigServer(query_list[1])
    if not config_server.valid:
        log.debug('invalid config has occurred')
        utils.socket_send(cs, 'warn: the config is invalid')
        return
    new_programs = mod_dash.load_programs(config_server.data)
    utils.thread_start(reload_launch_manager, (new_programs, ))
    # old_programs = dashboard.programs
    # nprog_names = list(new_programs.keys())
    # oprog_names = list(old_programs.keys())
    # for oprog_name, oprog in old_programs.items():
    #     if oprog_name not in nprog_names:
            # utils.thread_start(kill_program, (oprog, ))
    # ...


def serve_config(cs, query_list):
    print('do something !')


def serve_status(cs, query_list):
    log.info('serving: status: {0}'.format(query_list))
    if len(query_list) > 1:
        prog_names = query_list[1:]
    else:
        prog_names = list(dashboard.programs.keys())
        log.debug('something good')
    for prog_name in prog_names:
        utils.socket_send(cs, 'program status: {0}'.format(prog_name))
        program = dashboard.programs.get(prog_name)
        for process in program.processes:
            utils.socket_send(cs, '\t{0} status {1}'.format(process.name, process.state))


def serve_log(cs, query_list):
    print('do something !')


def serve_attach(cs, query_list):
    print('do something !')


def serve_shutdown(cs, query_list):
    log.info("Shutting down !")
    stop_programs(cs, dashboard.programs.keys())
    utils.socket_send(cs, 'Shutting down all programs!')
