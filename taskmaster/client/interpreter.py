import cmd
import os, sys
from taskmaster.common import config as tm_config
from taskmaster.utils import log

from taskmaster.client.client import Client
from taskmaster.client.tm_cmd import TaskmasterCmd



if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     client = Client(sys.argv[0])
    # else:
    #     client = Client(None)
    client = Client('../resources/config_temp.yml')
    if client.start() == False:
        print("STOP")
    # TaskmasterCli().cmdloop()
    tm_client = TaskmasterCmd('Hello>$ ')
    tm_client.cmdloop()