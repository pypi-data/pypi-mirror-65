# -*- coding: utf-8 -*-
from . import BaseRESTAPI
from .. import TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL


class Authen(BaseRESTAPI):
    """身份验证

    """
    pass

    # def authen_access_token(self):
    #     """获取登录用户身份
    #
    #     https://open.feishu.cn/document/ukTMukTMukTM/uEDO4UjLxgDO14SM4gTN
    #     """
    #     return self._post(
    #         'authen/v1/access_token',
    #         data={
    #             "app_access_token": self._client.access_token(TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL),
    #             "grant_type": "authorization_code",
    #             "code": "7804a6151b17f4f2"
    #         }
    #     )

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

    # def role_list(self):
    #     """获取角色列表
    #
    #     https://open.feishu.cn/document/ukTMukTMukTM/uYzMwUjL2MDM14iNzATN
    #     """
    #     return self._get(
    #         'contact/v2/role/list',
    #         params={
    #         },
    #         token_type=TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL
    #     )
