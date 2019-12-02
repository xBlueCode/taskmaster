import socket
from taskmaster.utils import log

log = log.get_logger('service_manager')

def service_manager(cs:socket.socket, addr, config):
    cmd = cs.recv(1024).decode('utf-8')
    if cmd == 'auth':
        username, auth = authenticate_client(cs, addr, config)
    else:
        log.debug('Not expected cmd from the clinet {0}'.format(cmd))
        return
    if not auth:
        log.info('client {0} failed to authenticate'.format(username))
        return


def authenticate_client(cs, addr, configServer) -> (str, bool):
    username = cs.recv(256).decode('utf-8')
    password = cs.recv(256).decode('utf-8')
    if username not in configServer.clients.keys():
        return username, False
    elif password != configServer.clients.get(username):
        return username, False
    else:
        return username, True
