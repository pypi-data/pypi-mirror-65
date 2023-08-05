from json import load
class ConfigurationFileException(Exception):
    pass
try:
    with open('.chimerarc') as f:
        configs = load(f)
except FileNotFoundError as e:
    print(f'Unable to find chimerarc file. Maybe missing \'chimera init\'?')
    exit(1)
