import threading


def thread_start(target, args):
    thread = threading.Thread(target=target, args=args)
    thread.start()
