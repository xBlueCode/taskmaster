import cmd
import os, sys
from taskmaster.common import config as tm_config
from taskmaster.utils import log
from taskmaster.client.tm_cmd import TaskmasterCmd
from getpass import getpass
import socket


log = log.get_logger('client')

ATTEMPT_MAX = 3

class Client():

    def __init__(self, configFile : str = None):
        self.config = tm_config.ConfigClient(configFile)
        self.csocket = socket.socket()

    def start(self):

        print('Starting the client ...')
        if not self.connect():
            return -1
        if not self.try_authenticate():
            return -1
        return self.cli()

    def connect(self) -> bool:
        # return True #  test
        if not self.config.host:
            self.config.host = input("Enter host ip: ")
        if not self.config.port:
            self.config.port = input("Enter port: ")
        try:
            self.csocket.connect((self.config.host, self.config.port))
            print('connected to the server ({0}:{1})'
                  .format(self.config.host, self.config.port))
            return True
        except:
            print('failed to connect the server ({0}:{1})'
                  .format(self.config.host, self.config.port), file=sys.stderr)
            return False

    def try_authenticate(self) -> bool:
        attempt = ATTEMPT_MAX
        while attempt > 0:
            if self.authenticate():
                print('client authenticated successfully on the server')
                return True
            else:
                attempt -= 1
        print("failed to authenticate on the server", file= sys.stderr)
        return False

    def authenticate(self) -> bool:
        if not self.config.username:
            self.config.username = input("Enter username: ")
        if not self.config.password:
            # self.config.password = getpass("Enter password: ")
            self.config.password = input("Enter password: ")
        query = 'auth\r\n{0}\r\n{1}\r\n'\
            .format(self.config.username, self.config.password)
        self.csocket.send(query.encode('utf-8'))
        response = self.csocket.recv(1024).decode('utf-8')
        log.debug('received {0} from server'.format(response))
        response = response.rsplit('\r\n')
        log.debug('response list {0}'.format(response))
        if response[0] != 'OK':
            log.info('failed to authenticate with response: {0}'.format(response[0]))
            self.config.password = None
            return False
        return True

    def cli(self):
        cmd = TaskmasterCmd('Hello>$ ')
        cmd.cmdloop()
        return 0
