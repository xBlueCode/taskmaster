import cmd
import os
from taskmaster.common import config as tm_config
from taskmaster.utils import log
from getpass import getpass
import socket

log = log.get_logger('server')

class Client():

    def __init__(self, configFile : str = None):
        self.config = tm_config.ConfigClient(configFile)

    def start(self):
        log.info('running the client daemon')
        attempt = 0
        while True:
            if self.connect() == False:
                attempt += 1
                log.error('failed connection to server. Attempt:'+attempt)
                if attempt == 3:
                    return False
            else:
                break
        log.info('created connection to server')
        attempt = 0
        while True:
            if not self.authenticate():
                attempt += 1
                log.error('failed authentication to server. Attempt:'+attempt)
                if attempt == 3:
                    return False
            else:
                break
        log.info('authenticated to server')

    def connect(self):
        if not self.config.host:
            self.config.host = input("Enter host ip: ")
        if not self.config.port:
            self.config.port = input("Enter port: ")
        # if not socket.create_connection((self.config.host, self.config.host)):
        #     print('Failed connection to server.')
        return True

    def authenticate(self):
        if not self.config.username:
            self.config.username = input("Enter username: ")
        if not self.config.password:
            self.config.password = getpass("Enter password: ")
        # if not socket.AUTHENTIFICATE(username + password):
        #     print('Failed to authentificate user'+self.config.username)
        #     return False
        return True
