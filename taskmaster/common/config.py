import yaml

from taskmaster.utils import log

logger_std = log.get_logger('config')

section_base = ['connection']
section_server = ['server', 'programs']
section_client = ['client']

client_attr = {
    'prompt': str,
    'host': str,
    'port': int,
    'username': str,
    'password': str
}


class Config:
    """\
    Basic configuration class which contain the information from the config file
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load()
        self.valid = True
        if self.data is None:
            logger_std.error('Failed to load config file')
            self.valid = False
            return
        self.valid = self.parse_sections(section_base)
        if not self.valid:
            return
        logger_std.info('Config file has beeen loaded successfully')

    def load(self) -> dict:
        """\
        Loads the yaml file
        :return: configuration data from the yaml file
        """
        data = None
        try:
            with open(self.filepath, 'r') as cfile:
                data = yaml.load(cfile, Loader=yaml.FullLoader)
                cfile.close()
        except Exception as e:
            logger_std.error('Failed to open config file', exc_info=log.EXC_INFO)
        return data

    def save(self):
        """
        Save the provided data to a yaml file with the saved path
        :return: None
        """
        with open(self.filepath, 'w') as cfile:
            yaml.dump(self.data, cfile)

    def parse_sections(self, sections: [str]) -> object:
        for section in sections:
            if section not in self.data.keys():
                logger_std.error('{0} section must be present in the config file'.format(section))
                return False
            setattr(self, section, self.data.get(section))
        return True


class ConfigServer(Config):
    def __init__(self, filepath):
        super().__init__(filepath)
        if not self.valid:
            logger_std.error('failed to create a valid Server Config')
            return
        self.valid = self.parse_sections(section_server)
        if not self.valid:
            logger_std.error('failed to create a valid Server Config')
            return


class ConfigClient(Config):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.prompt = None
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        if not self.valid:
            logger_std.error('failed to create a valid Client Config')
            return
        self.valid = self.parse_sections(section_client)
        if not self.valid:
            logger_std.error('failed to create a valid Client Config')
            return
        for cattr, ctype in client_attr.items():
            val = self.client.get(cattr)
            if val and isinstance(val, ctype):
                setattr(self, cattr, val)


def load(filepath):
    """\
    Loads the yaml file
    :param filepath: the path to the yaml file
    :return: configuration data from the yaml file
    """
    data = None
    try:
        with open(filepath, 'r') as cfile:
            data = yaml.load(cfile, Loader=yaml.FullLoader)
            cfile.close()
    except Exception as e:
        logger_std.error('Failed to open config file', exc_info=log.EXC_INFO)
    return data


def save(filepath, data):
    """
    Save the provided data to a yaml file with the provide path
    :param filepath:
    :param data:
    :return: None
    """
    with open(filepath, 'w') as cfile:
        yaml.dump(data, cfile)
