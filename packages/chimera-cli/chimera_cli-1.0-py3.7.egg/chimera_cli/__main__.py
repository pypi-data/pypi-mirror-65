from chimera_cli.parsing import main_parser
from chimera_cli.api import chimera_rest_api
from chimera_cli.yaml_config import configuration_files

if __name__ == "__main__":
    config = main_parser.parse_args()
    if config.command == 'deploy':
        files = configuration_files()
        