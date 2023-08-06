# -*- coding: utf-8 -*-
from . import BaseRESTAPI
from .. import TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL


class Contact(BaseRESTAPI):
    """通讯录

    """

    def scope_get(self):
        """获取通讯录授权范围

        https://open.feishu.cn/document/ukTMukTMukTM/ugjNz4CO2MjL4YzM
        """
        return self._get(
            'contact/v1/scope/get',
            params={
            }
        )

    """用户管理
    
    """

    # def x(self):
    #     """批量获取用户信息
    #
    #     https://open.feishu.cn/document/ukTMukTMukTM/uIzNz4iM3MjLyczM
    #     """
    #     return self._get(
    #         'contact/v1/scope/get',
    #         params={
    #         }
    #     )

    # def x(self):
    #     """获取部门用户列表
    #
    #     https://open.feishu.cn/document/ukTMukTMukTM/uEzNz4SM3MjLxczM
    #     """
    #     return self._get(
    #         'contact/v1/department/user/list',
    #         params={
    #         }
    #     )




    def role_list(self):
        """获取角色列表

        https://open.feishu.cn/document/ukTMukTMukTM/uYzMwUjL2MDM14iNzATN
        """
        return self._get(
            'contact/v2/role/list',
            params={
            },
            token_type=TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL
        )
