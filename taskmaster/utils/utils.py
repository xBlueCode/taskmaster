import threading
import socket

SOCKET_HEAD = 10


def thread_start(target, args):
    thread = threading.Thread(target=target, args=args)
    thread.start()


def socket_bind(socket: socket.socket, addr) -> bool:
    try:
        socket.bind(addr)
        socket.listen(5)
        return True
    except:
        return False


def socket_recv(socket: socket.socket) -> str:
    try:
        size = socket.recv(SOCKET_HEAD).decode('utf-8')
        size = int(size)
        if size < 1:
            return ''
        data = socket.recv(size).decode('utf-8')
        return data
    except ConnectionResetError as err:
        raise ConnectionResetError


def socket_send(socket: socket.socket, data: str):
    try:
        bytes = data.encode('utf-8')
        if data == '':
            size = 0
        else:
            size = len(bytes)
        head = '{0:010d}'.format(size)
        socket.send(head.encode('utf-8'))
        if size > 0:
            socket.send(bytes)
    except :
        return
