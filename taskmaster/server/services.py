
from taskmaster.utils import log

from taskmaster.utils import utils

log = log.get_logger('services')


def serve_start(cs, query):
    log.info('serving: start')
    utils.socket_send(cs, 'something there from start')
    utils.socket_send(cs, '\r')
