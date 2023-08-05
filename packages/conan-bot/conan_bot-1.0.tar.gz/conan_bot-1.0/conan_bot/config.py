import configparser


class MyException(Exception):
    pass


class BotConfig(configparser.ConfigParser):
    def __init__(self, config_file):
        super(BotConfig, self).__init__()
        self.read(config_file)
        self.validate_config()

    def validate_config(self):
        section = None
        keys = None

        required_values = {
            'discord': {
                'token': None,
                'channel': None,
            },
            'server': {
                'ip': None,
                'port': None,
                'name': None,
            }
        }

        for section, keys in required_values.items():
            if section not in self:
                raise MyException(
                    'Missing section %s in the config file' % section)

        for key, values in keys.items():
            if key not in self[section] or self[section][key] == '':
                raise MyException((
                                          'Missing value for %s under section %s in ' +
                                          'the config file') % (key, section))

            if values:
                if self[section][key] not in values:
                    raise MyException((
                                              'Invalid value for %s under section %s in ' +
                                              'the config file') % (key, section))


config = {}

try:
    config = BotConfig('conan-bot.ini')
except MyException as e:
    print(e)
    exit(1)
