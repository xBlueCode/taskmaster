import cmd
import os, sys
from taskmaster.common import config as tm_config
from taskmaster.utils import log

from taskmaster.client.client import Client

class TaskmasterCmd(cmd.Cmd):
    def __init__(self, prompt: str = '(taskmaster)$> '):
        super.__init__()
        self.prompt = prompt

    # intro = 'Welcome to the taskmaster shell.   Type help or ? to list commands.\n'
    # prompt = '(taskmaster)$> '

    def default(self, line):
        print("return value : " + line)

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