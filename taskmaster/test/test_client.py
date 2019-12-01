
from taskmaster.common import config as tm_config


if __name__ == '__main__':
    client = tm_config.ConfigClient("../resources/config_temp.yml")

    print(client.prompt)
