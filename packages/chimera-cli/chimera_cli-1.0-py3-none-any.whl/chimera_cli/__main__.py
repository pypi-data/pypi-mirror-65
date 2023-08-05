from chimera_cli.parsing import main_parser
from chimera_cli.yaml_config import configuration_files
import pprint
from json import dump
from os import mkdir
from .build import Deploy, BuildAll, TagAll, Watch

def parse_pipeline(yaml):
    pipeline = {}
    pipeline['name'] = yaml['name']
    pipeline['nodes'] = []
    for node in yaml['apps']:
        current = yaml['apps'][node]
        parsed = {}
        try:
            parsed['inputs'] = current['inputs']
        except:
            parsed['inputs'] = []
        try:
            parsed['outputs'] = current['outputs']
        except:
            parsed['outputs'] = []
        parsed['name'] = node
        try:
            current['expose']
        except:
            parsed['service'] = {'exposed': False, 'port': 0}
        else:
            parsed['service'] = {'exposed': True,
                                 'port': int(current['expose'])}
        try:
            parsed['replicas'] = int(current['replicas'])
        except:
            parsed['replicas'] = 3
        parsed['build'] = current['build']
        try:
            parsed['env'] = list(
                map(lambda x: {'name': x, 'value': str(current['env'][x])}, current['env']))
        except Exception as e:

            parsed['env'] = []

        pipeline['nodes'] += [parsed]
    return pipeline


if __name__ == "__main__":
    config = main_parser.parse_args()

    if config.command == 'deploy':
        from chimera_cli.api import chimera_rest_api

        files = configuration_files()
        if config.subcommand == None:
            for f in files['channel']:
                if config.namespace != None and f['namespace'] != config.namespace:
                    continue
                if f['type'] == 'channel':
                    for key in f['channels'].keys():
                        chimera_rest_api.create_channel(
                            key, f['namespace'], f['channels'][key])
                        print(
                            "Channel {} created in namespace {}!".format(
                                key, f['namespace']
                            )
                        )
            for f in files['pipeline']:
                pipe = parse_pipeline(f)
                TagAll(pipe)
                BuildAll(pipe)
                Deploy(pipe, f['name'], f['namespace'])
                
        elif config.subcommand == 'channel':
            for f in files['channel']:
                if config.namespace != None and f['namespace'] != config.namespace:
                    continue
                for key in f['channels'].keys():
                    if config.name != None and config.name != key:
                        continue
                    chimera_rest_api.create_channel(
                        key,
                        f['namespace'],
                        f['channels'][key]
                    )
                    print(
                        "Channel {} created in namespace {}!".format(
                            key, f['namespace']
                        )
                    )
        elif config.subcommand == 'pipeline':
            for f in files['pipeline']:
                if config.namespace != None and config.namespace != f['namespace']:
                    continue
                if config.name != None and config.name != f['name']:
                    continue
                from .build import TagAll, BuildAll
                pipe = parse_pipeline(f)
                TagAll(pipe)
                BuildAll(pipe)
                Deploy(pipe, f['name'], f['namespace'])

    elif config.command == 'delete':
        from chimera_cli.api import chimera_rest_api

        if config.subcommand == 'namespace':
            chimera_rest_api.delete_namespace(config.namespace)
            print("Namespace {} deleted!".format(config.namespace))

        if config.subcommand == 'channel':
            chimera_rest_api.delete_channel(config.name, config.namespace)
            if config.name != None:
                print(
                    "Channel {} from namespace {} deleted!".format(
                        config.name,
                        config.namespace
                    )
                )

            else:
                print(
                    "All channels from namespace {} deleted!".format(
                        config.namespace
                    )
                )
        if config.subcommand == 'pipeline':
            chimera_rest_api.delete_pipeline(config.name, config.namespace)
            if config.name != None:
                print(
                    "Pipeline {} from namespace {} deleted!".format(
                        config.name,
                        config.namespace
                    )
                )

            else:
                print(
                    "All pipelines from namespace {} deleted!".format(
                        config.namespace
                    )
                )

    elif config.command == 'get':
        from chimera_cli.api import chimera_rest_api
        if config.subcommand == 'channel':
            log = chimera_rest_api.get_channel_logs(
                config.name, config.namespace)
            pprint.pprint(log)

        if config.subcommand == 'pipeline':
            pprint.pprint(chimera_rest_api.get_pipeline_logs(
                config.name, config.namespace))

    elif config.command == 'watch':
        files = configuration_files()

        from .build import Watch
        Watch(files)        

    elif config.command == 'init':
        url = input('Enter the url for your chimera cluster:')
        username = input('Enter the username for your chimera cluster:')
        password = input('Enter the password for your chimera cluster:')
        with open('.chimerarc', 'w') as f:
            dump(
                {
                    "clusterUrl": url,
                    "username": username,
                    "password": password
                }, f, indent=4)
        mkdir('.chimera')
