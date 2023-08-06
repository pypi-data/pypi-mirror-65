from controller.client import Client
from typing import List
from urllib.parse import urlparse
from .device import Device

import logging

logger = logging.getLogger('fgp.model.application')


class Application:
    _client: Client

    url: str = None
    name: str = None
    references: List = None
    devices: List = None

    @classmethod
    def from_dict(cls, d) -> 'Application':
        a = Application()
        a.url = d.get('links', {}).get('self', '')
        a.name = urlparse(a.url).path.replace('/', '')
        a.references = list()
        a.devices = list()
        for item in d.get('data'):
            path = list(item.keys())[0]
            object_type = item[path]
            if object_type == 'reference':
                a.references.append(path)
            elif object_type == 'device':
                a.devices.append(path)
            else:
                logger.warning(f'Unknown object type {object_type}')
        return a

    def reload_script(self):
        return self._client.post('{self.name}/reload_script')

    def device(self, device_name) -> Device:
        ret = self._client.post(f'{self.name}/{device_name}')
        return Device()

    def reference(self, reference_name) -> 'Reference':
        pass