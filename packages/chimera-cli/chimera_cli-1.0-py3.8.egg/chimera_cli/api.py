from requests import post, get
from chimera_cli.configuration import configs
from json import load
from typing import Any
import avro.io as avro
import avro.schema as avsc
import io

__pipeline_schema__ = """{
   "type": "record",
   "name": "pipeline",
   "namespace": "inspr.com",
   "fields": [
      {
         "name": "name",
         "type": "string"
      },
      {
         "name": "nodes",
         "type": {
            "type": "array",
            "items": {
               "name": "nodes",
               "type": "record",
               "namespace": "inspr.com",
               "fields": [
                  {
                     "name": "name",
                     "type": "string"
                  },
                  {
                     "name": "image",
                     "type": "string"
                  },
                  {
                     "name": "inputs",
                     "type": {
                        "type": "array",
                        "items": "string"
                     }
                  },
                  {
                     "name": "outputs",
                     "type": {
                        "type": "array",
                        "items": "string"
                     }
                  }
               ]
            }
         }
      }
   ]
}"""

class ClusterURLException(Exception):
    pass

class ChimeraException(Exception):
    pass

class chimera_rest_api:
    """API for reaching chimera and sending and receiving information"""
    url: str = configs['clusterUrl']
    @staticmethod
    def create_channel(name: str, namespace: str, schema_path: str):
        """Creates a channel in the chimera cluster"""
        try:
            with open(f".chimera/{schema_path}") as f:
                schema = load(f)
        except Exception as e:
            raise ChimeraException(f'Schema path invalid! - {e}')
        try:
            response = post(f'http://{chimera_rest_api.url}/channel/{namespace}/{name}', json=schema)
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')
        print(response.text)
    
    @staticmethod
    def delete_channel(name: str, namespace: str):
        """Deletes a channel in the chimera cluster"""
        try:
            response = post(f'http://{chimera_rest_api.url}/delete/channel/{namespace}/{name}')
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')
    
    @staticmethod
    def create_pipeline(name: str, namespace: str, pipeline: Any):
        """Creates a pipeline in the chimera cluster"""

        parsed_schema = avsc.Parse(__pipeline_schema__)
        avrowriter = avro.DatumWriter(parsed_schema)
        bytes_writer = io.BytesIO()
        encoder = avro.BinaryEncoder(bytes_writer)
        avrowriter.write(pipeline, encoder)

        value = bytes_writer.getvalue()



        try:
            response = post(f'http://{chimera_rest_api.url}/pipeline/{namespace}/{name}', data=value)
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster\n{e}')

    @staticmethod
    def delete_pipeline(name: str, namespace: str):
        """Deletes a pipeline in the chimera cluster"""
        try:
            response = post(f'http://{chimera_rest_api.url}/delete/pipeline/{namespace}/{name}')
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')

    @staticmethod
    def delete_namespace(namespace: str):
        """Deletes a namespace in the chimera cluster"""
        try:
            response = post(f'http://{chimera_rest_api.url}/delete/namespace/{namespace}')
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text()}')
    
    @staticmethod
    def get_namespace_logs(namespace: str):
        try:
            response = get(f'http://{chimera_rest_api.url}/namespace/{namespace}')
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text}')
    
    @staticmethod
    def get_channel_logs(name: str = None, namespace: str = None):
        response = None
        if name == None:
            if namespace == None:
                try:
                    response = get(f'http://{chimera_rest_api.url}/channel')
                except Exception as e:
                    raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
            else:
                try:
                    response = get(f'http://{chimera_rest_api.url}/channel/{namespace}')
                except Exception as e:
                    raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
                
        else:
            if namespace == None:
                raise ChimeraException('Nil namespace')
            try:
                response = get(f'http://{chimera_rest_api.url}/channel/{namespace}/{name}')
            except Exception as e:
                raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text}')
        return response.json()
    
    @staticmethod
    def get_pipeline_logs(name: str = None, namespace: str = None):
        response = None
        if name == None:
            if namespace == None:
                try:
                    response = get(f'http://{chimera_rest_api.url}/pipeline')
                except Exception as e:
                    raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
            else:
                try:
                    response = get(f'http://{chimera_rest_api.url}/pipeline/{namespace}')
                except Exception as e:
                    raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
                
        else:
            if namespace == None:
                raise ChimeraException('Nil namespace')
            try:
                response = get(f'http://{chimera_rest_api.url}/pipeline/{namespace}/{name}')
            except Exception as e:
                raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(f'Cluster response invalid! - {response.text}')
        return response.json()
    