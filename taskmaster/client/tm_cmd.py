import cmd
import os, sys
from taskmaster.common import config as tm_config
from taskmaster.utils import log
from taskmaster.utils import utils


class TaskmasterCmd(cmd.Cmd):
    def __init__(self, client, prompt: str = '(taskmaster)$> '):
        from taskmaster.client.client import Client
        cmd.Cmd.__init__(self)
        self.client = client
        self.prompt = prompt

    # intro = 'Welcome to the taskmaster shell.   Type help or ? to list commands.\n'
    # prompt = '(taskmaster)$> '

    def default(self, line):
        query = "{0}".format(line)
        # self.client.csocket.send(query.encode('utf-8'))
        # response = self.client.csocket.recv(1024).decode('utf-8')
        utils.socket_send(self.client.csocket, query)
        while True:
            response = utils.socket_recv(self.client.csocket)
            if response == '' or response == '\r':
                break
            print(response)

    def do_shelltaskmaster(self, line):
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)

    def do_args(self, args):
        print(args)

    def do_exit(self, line):
        "Exit"
        return True

    def do_EOF(self, line):
        "Exit with Ctrl-D"
        return True
