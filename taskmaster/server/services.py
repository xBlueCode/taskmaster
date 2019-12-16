
from taskmaster.utils import log

from taskmaster.utils import utils

from taskmaster.server.dashboard import dashboard

log = log.get_logger('services')


def serve_start(cs, query_list):
    log.info('serving: start')
    # utils.socket_send(cs, 'something there from start')
    # utils.socket_send(cs, '\r')
    prog_names = query_list[1:]
    log.debug('prog_names: {0}'.format(prog_names))
    for prog_name in prog_names:
        if prog_name not in dashboard.programs.keys():
            utils.socket_send(cs, 'program {0} not found'.format(prog_name))
        else:
            utils.socket_send(cs, 'starting {0}'.format(prog_name))