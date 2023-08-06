from typing import List, Dict
from .client import Client
from fgp.model.model import FGModel
import urllib.parse


class Reference:

    _client: Client = None

    def __init__(self, client: Client):
        self._client = client

    def query(
            self,
            reference_name: str,
            query: str,
            order_by: str=None,
            limit: int=100,
            page: int=0
        ) -> List[Dict[str, str]]:
        if query:
            query_parsed = urllib.parse.quote(query)
        else:
            query_parsed = ""
        res = self._client.get(route=f'{reference_name}/data/{limit}/{page}/{order_by}{query_parsed}')
        # data = self.parse_get_data(res)
        return res

    def get_schema(self, reference_name) -> FGModel:
        data = self._client.get(route=f'{reference_name}')
        return FGModel.from_object(reference_name, data.get('links', {}).get('persistenceInfo', []))

