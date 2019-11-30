import threading


def thread_start(target, args):
    thread = threading.Thread(target=target, args=args)
    thread.start()


def socket_bind(socket, addr) -> bool:
    try:
        socket.bind(addr)
        socket.listen(5)
        return True
    except:
        return False
