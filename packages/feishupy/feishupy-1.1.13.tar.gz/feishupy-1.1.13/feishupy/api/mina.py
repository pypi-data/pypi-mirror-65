# -*- coding: utf-8 -*-
from . import BaseRESTAPI


class Mina(BaseRESTAPI):
    """Mina

    """

    def code2session(self, code):
        """code2session

        https://open.feishu.cn/document/ukTMukTMukTM/ukjM04SOyQjL5IDN
        """
        return self._post(
            'mina/v2/tokenLoginValidate',
            data={'code': code}
        )
