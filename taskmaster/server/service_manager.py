import socket
from taskmaster.utils import log

log = log.get_logger('service_manager')


def service_manager(cs:socket.socket, addr, config):
    username, auth = authenticate_client(cs, addr, config)
    if not auth:
        log.info('client {0} failed to authenticate'.format(username))
        return
    serve_client(cs, addr, config)


def authenticate_client(cs, addr, configServer) -> (str, bool):
    # username = cs.recv(256).decode('utf-8')
    # password = cs.recv(256).decode('utf-8')
    auth_query = cs.recv(1024).decode('utf-8')
    log.debug('received auth query: {0}'.format(auth_query))
    auth_list = auth_query.rsplit('\r\n')
    log.debug('auth list: {0}'.format(auth_list))
    if len(auth_list) < 3 or auth_list[0] != 'auth':
        cs.send('KO-1'.encode('utf-8'))
        return None, False
    elif auth_list[1] not in configServer.clients.keys():
        cs.send('KO-2'.encode('utf-8'))
        return auth_list[1], False
    elif auth_list[2] != configServer.clients.get(auth_list[1]):
        cs.send('KO-3'.encode('utf-8'))
        return auth_list[1], False
    else:
        cs.send('OK'.encode('utf-8'))
        return auth_list[1], True


def serve_client(cs, addr, configServer):
    while True:
        query = cs.recv(1024).decode('utf-8')
        query_list = query.rsplit('\r\n')
        log.info('query: {0}'.format(query_list))

