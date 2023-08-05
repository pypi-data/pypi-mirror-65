from chimera_cli.configuration import configs
from requests import post, get, delete
from requests.auth import HTTPBasicAuth
from json import load
from typing import Any
import avro.io as avro
import avro.schema as avsc
import io

__pipeline_schema__ = """{
    "type": "record",
    "name": "pipeline",
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
                    "type": "record",
                    "name": "node",
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
                            "name": "replicas",
                            "type": "int"
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
                        },
                        {
                            "name": "env",
                            "type": {
                                "type": "array",
                                "items": {
                                    "type": "record",
                                    "name": "environment",
                                    "fields": [
                                        {
                                            "name": "name",
                                            "type": "string"
                                        },
                                        {
                                            "name": "value",
                                            "type": "string"
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "name": "service",
                            "type": {
                                "type": "record",
                                "name": "port",
                                "fields": [
                                    {
                                        "name": "exposed",
                                        "type": "boolean"
                                    },
                                    {
                                        "name": "port",
                                        "type": "int"
                                    }
                                ]
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
    httpAuth = HTTPBasicAuth(configs['username'], configs['password'])
    @staticmethod
    def create_channel(name: str, namespace: str, schema_path: str):
        """Creates a channel in the chimera cluster"""
        try:
            with open(f".chimera/{schema_path}") as f:
                schema = load(f)
        except Exception as e:
            raise ChimeraException(f'Schema path invalid! - {e}')
        try:
            response = post(
                f'http://{chimera_rest_api.url}/channel/{namespace}/{name}',
                auth=chimera_rest_api.httpAuth,
                json=schema
            )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')
        print(response.text)

    @staticmethod
    def delete_channel(name: str, namespace: str):
        """Deletes a channel in the chimera cluster"""
        try:
            if name == None:
                response = delete(
                    f'http://{chimera_rest_api.url}/channel/{namespace}',
                    auth=chimera_rest_api.httpAuth
                )
            else:
                response = delete(
                    f'http://{chimera_rest_api.url}/channel/{namespace}/{name}',
                    auth=chimera_rest_api.httpAuth
                )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')

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
            response = post(
                f'http://{chimera_rest_api.url}/pipeline/{namespace}/{name}',
                auth=chimera_rest_api.httpAuth,
                data=value
            )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster\n{e}')

        if response.status_code != 200:
            raise ChimeraException(response.text)

    @staticmethod
    def delete_pipeline(name: str, namespace: str):
        """Deletes a pipeline in the chimera cluster"""
        try:
            if name == None:
                response = delete(
                    f'http://{chimera_rest_api.url}/pipeline/{namespace}',
                    auth=chimera_rest_api.httpAuth
                )
            else:
                response = delete(
                    f'http://{chimera_rest_api.url}/pipeline/{namespace}/{name}',
                    auth=chimera_rest_api.httpAuth
                )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')

    @staticmethod
    def delete_namespace(namespace: str):
        """Deletes a namespace in the chimera cluster"""
        try:
            response = delete(
                f'http://{chimera_rest_api.url}/namespace/{namespace}',
                auth=chimera_rest_api.httpAuth
            )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')

    @staticmethod
    def get_namespace_logs(namespace: str):
        try:
            response = get(
                f'http://{chimera_rest_api.url}/namespace/{namespace}',
                auth=chimera_rest_api.httpAuth
            )
        except Exception as e:
            raise ChimeraException(f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')
        return response.json()

    @staticmethod
    def get_channel_logs(name: str = None, namespace: str = None):
        response = None
        if name == None:
            if namespace == None:
                try:
                    response = get(
                        f'http://{chimera_rest_api.url}/channel',
                        auth=chimera_rest_api.httpAuth
                    )
                except Exception as e:
                    raise ChimeraException(
                        f'Unable to reach chimera cluster \n{e}')
            else:
                try:
                    response = get(
                        f'http://{chimera_rest_api.url}/channel/{namespace}',
                        auth=chimera_rest_api.httpAuth
                    )
                except Exception as e:
                    raise ChimeraException(
                        f'Unable to reach chimera cluster \n{e}')

        else:
            if namespace == None:
                raise ChimeraException('Nil namespace')
            try:
                response = get(
                    f'http://{chimera_rest_api.url}/channel/{namespace}/{name}',
                    auth=chimera_rest_api.httpAuth
                )
            except Exception as e:
                raise ChimeraException(
                    f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')
        return response.json()

    @staticmethod
    def get_pipeline_logs(name: str = None, namespace: str = None):
        response = None
        if name == None:
            if namespace == None:
                try:
                    response = get(
                        f'http://{chimera_rest_api.url}/pipeline',
                        auth=chimera_rest_api.httpAuth
                    )
                except Exception as e:
                    raise ChimeraException(
                        f'Unable to reach chimera cluster \n{e}')
            else:
                try:
                    response = get(
                        f'http://{chimera_rest_api.url}/pipeline/{namespace}',
                        auth=chimera_rest_api.httpAuth
                    )
                except Exception as e:
                    raise ChimeraException(
                        f'Unable to reach chimera cluster \n{e}')

        else:
            if namespace == None:
                raise ChimeraException('Nil namespace')
            try:
                response = get(
                    f'http://{chimera_rest_api.url}/pipeline/{namespace}/{name}',
                    auth=chimera_rest_api.httpAuth
                )
            except Exception as e:
                raise ChimeraException(
                    f'Unable to reach chimera cluster \n{e}')
        if response.status_code != 200:
            raise ChimeraException(
                f'Cluster response invalid! - {response.text}')
        return response.json()
