from json import load
class ConfigurationFileException(Exception):
    pass
try:
    with open('.chimerarc') as f:
        configs = load(f)
except Exception as e:
    raise ConfigurationFileException(f'Unable to read configuration file - {e}')
