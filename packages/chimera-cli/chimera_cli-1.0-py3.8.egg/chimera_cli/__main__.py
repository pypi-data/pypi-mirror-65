from chimera_cli.parsing import main_parser
from chimera_cli.api import chimera_rest_api
from chimera_cli.yaml_config import configuration_files


def parse_pipeline(yaml):
    pipeline = {}
    pipeline['name'] = yaml['name']
    pipeline['nodes'] = []
    for node in yaml['apps']:
        try:
            yaml['apps'][node]['inputs']
        except:
            yaml['apps'][node]['inputs'] = []
        try:
            yaml['apps'][node]['outputs']
        except:
            yaml['apps'][node]['outputs'] = []
        
        parsed = yaml['apps'][node]
        parsed['name'] = node
        pipeline['nodes'] += [parsed]
    return pipeline

if __name__ == "__main__":
    config = main_parser.parse_args()

    if config.command == 'deploy':
        files = configuration_files()
        if config.subcommand == None:
            pipelines = []
            for f in files:
                if config.namespace != None and f['namespace'] != config.namespace:
                    continue
                if f['type'] == 'channel':
                    for key in f['channels'].keys():
                        chimera_rest_api.create_channel(key, f['namespace'], f['channels'][key])
                else:
                    pipelines += [f]
            for f in pipelines:
                chimera_rest_api.create_pipeline(f['name'], f['namespace'], parse_pipeline(f))
        elif config.subcommand == 'channel':
            for f in files['channel']:
                if config.namespace != None and f['namespace'] != config.namespace:
                    continue
                for key in f['channels'].keys():
                    if config.name != None and config.name != key:
                        continue
                    chimera_rest_api.create_channel(key, f['namespace'], f['channels'][key])
        elif config.subcommand == 'pipeline':
            for f in files['pipeline']:
                if config.namespace != None and config.namespace != f['namespace']:
                    continue
                if config.name != None and config.name != f['name']:
                    continue
                chimera_rest_api.create_pipeline(f['name'], f['namespace'], parse_pipeline(f))
                    
    elif config.command == 'delete':
        if config.subcommand == 'namespace':
            chimera_rest_api.delete_namespace(config.namespace)
        if config.subcommand == 'channel':
            chimera_rest_api.delete_channel(config.name, config.namespace)
        if config.subcommand == 'pipeline':
            chimera_rest_api.delete_pipeline(config.name, config.namespace)
    
    elif config.command == 'get':
        if config.subcommand == 'channel':
            log = chimera_rest_api.get_channel_logs(config.name, config.namespace)
            print(log)
        if config.subcommand == 'pipeline':
            chimera_rest_api.get_pipeline_logs(config.name, config.namespace)
                              


        