# -*- coding: utf-8 -*-

# Author: WUWUTech
# Contact: wuwu@wuwu.tech

"""A package for FeiShu, Implement API."""

from . import HttpClient, api, TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL
from .session import MemoryStorage


class FeiShuClient(object):

    def __init__(self, app_id, app_secret, session=None):
        self._app_id = app_id
        self._app_secret = app_secret
        self.session = session or MemoryStorage()

        self.client = HttpClient(self._app_id, self._app_secret, self.session)  # Default HttpClient
        self.contact = api.Contact(client=self.client)
        self.authen = api.Authen(client=self.client)
        self.mina = api.Mina(client=self.client)

    def access_token(self, token_type=TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL):
        return self.client.access_token(token_type)
