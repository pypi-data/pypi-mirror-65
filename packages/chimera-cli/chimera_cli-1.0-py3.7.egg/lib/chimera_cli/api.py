from requests import post, get
from chimera_cli.configuration import configs
from json import load
class ClusterURLException(Exception):
    pass

class ChimeraException(Exception):
    pass

class chimera_rest_api:
    url: str = configs.clusterUrl
    @staticmethod
    def create_channel(name: str, namespace: str, schema_path: str):
        try:
            with open(f".chimera/{schema_path}") as f:
                schema = load(f)
        except:
            raise ChimeraException(f'Schema path invalid! - {e}')
        try:
            response = post(f'{url}/channel/{namespace}/{name}', json=schema)
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')
    
    @staticmethod
    def delete_channel(name: str, namespace: str):
        try:
            response = post(f'{url}/delete/channel/{namespace}/{name}')
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')
    