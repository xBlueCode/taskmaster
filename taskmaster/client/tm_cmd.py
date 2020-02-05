import cmd
import os, sys, pathlib
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

    def do_config(self, line):
        cmds = line.split()
        if len(cmds) > 1:
            print("[!] Error too many arguments\nUsage : config [config_file]")
        elif (self.resolve_path(cmds[0]) == None):
            print("[!] Error incorrect path of file %s\nUsage : config [config_file]" % cmds[0])
        elif (not os.access(self.resolve_path(cmds[0]), os.R_OK)):
            print("[!] Error incorrect permission on config file\nAdd appropriate right"
                  " to %s" % self.resolve_path(cmds[0]))
        else:
            print("Good config file here %s sent throw socket" % self.resolve_path(cmds[0]))
            query = "{0}".format(line)
            utils.socket_send(self.client.csocket, query)

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

    def resolve_path(self, path):
        new_path = pathlib.Path(path)
        if new_path.is_file():
            return str(new_path.absolute())
        return None