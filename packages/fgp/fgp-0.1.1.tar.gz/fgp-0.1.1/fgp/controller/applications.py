from .client import Client
from fgp.model.application import Application
from typing import List


class Applications:
    _client: Client = None

    @classmethod
    def list_applications(cls):
        ret = cls.client.get('/')

    @classmethod
    def get_application(cls, application_name) -> Application:
        return Application.from_dict(cls.client.get(application_name))

    # @classmethod
    # def _parse_list_applications(cls, d: dict) -> List[Application]:
    #     for app in d.data:
    #         ret.append(Application)