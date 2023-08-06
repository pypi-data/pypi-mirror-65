from typing import List, Dict
from .client import Client
from fgp.model.model import FGModel
import urllib.parse


class Event:

    _client: Client = None

    def __init__(self, client: Client):
        self._client = client

    def update_event(
            self,
            device_type: str,
            device_name: str,
            stream_name: str,
            data: dict
        ) -> List[Dict[str, str]]:
        if type(data) is dict:
            data = [data]
        res = self._client.post(route=f'{device_type}/name/{device_name}/{stream_name}', data=data, params={'synchronous': True})
        return res

    def get_schema(self, reference_name) -> FGModel:
        data = self._client.get(route=f'{reference_name}')
        return FGModel.from_object(reference_name, data.get('links', {}).get('persistenceInfo', []))

