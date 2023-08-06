# -*- coding: utf-8 -*-

# Author: WUWUTech
# Contact: wuwu@wuwu.tech

import json
import requests

from . import TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL


class HttpClient(object):

    def __init__(self, app_id, app_secret, session, timeout=10, auto_retry=True):
        self._app_id = app_id
        self._app_secret = app_secret
        self._session = session
        self.timeout = timeout
        self.auto_retry = auto_retry

        self._http = requests.Session()

    def get(self, path, **kwargs):
        return self._request(
            method='get',
            url=self.get_url(path),
            **kwargs
        )

    def post(self, path, **kwargs):
        return self._request(
            method='post',
            url=self.get_url(path),
            **kwargs
        )

    def get_url(self, path):
        protocol = 'https'
        host = 'open.feishu.cn/open-apis'
        return '{protocol}://{host}/{path}'.format(protocol=protocol, host=host, path=path)

    def _request(self, method, url, **kwargs):
        if 'params' not in kwargs:
            kwargs['params'] = {}

        if isinstance(kwargs.get('data', ''), dict):
            body = (json.dumps(kwargs['data'], ensure_ascii=False)).encode('utf-8')
            kwargs['data'] = body

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        # headers = {'Authorization': 'Bearer {}'.format(self.access_token())}
        headers = kwargs.get('headers', {})
        if not headers.get('Authorization'):
            headers['Authorization'] = 'Bearer {}'.format(
                self.access_token(kwargs.get('token_type', TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL)))
        params = kwargs.get('params', {})
        data = kwargs.get('data', {})
        res = self._http.request(method=method, url=url, params=params, data=data, headers=headers)

        try:
            res.raise_for_status()
        except Exception as e:
            raise Exception('Http request error!')

        return self._handle_result(res, method, url, result_processor, **kwargs)

    def _handle_result(self, res, method=None, url=None, result_processor=None, **kwargs):
        if not isinstance(res, dict):  # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        return result if not result_processor else result_processor(result)

    @staticmethod
    def _decode_result(res):
        try:
            result = json.loads(res.content.decode('utf-8', 'ignore'), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            print('Can not decode response as JSON!')
            return res
        return result

    def access_token_key(self, _app_id, token_type):
        return "{}_{}".format(_app_id, token_type)

    def access_token(self, _token_type):
        access_token_key = self.access_token_key(self._app_id, _token_type)
        access_token = self._session.get(access_token_key)
        if not access_token:
            expires_in = 7200
            result = self.fetch_access_token(_token_type, self._app_id, self._app_secret)
            if "expire" in result:
                expires_in = result["expire"]
            self._session.set(access_token_key, result["app_access_token"], expires_in)
            access_token = self._session.get(access_token_key)
        return access_token

    def fetch_access_token(self, token_type, app_id, app_secret):
        """
        获取 access token
        详情请参考
            获取 app_access_token（企业自建应用）
                https://open.feishu.cn/document/ukTMukTMukTM/uADN14CM0UjLwQTN
            获取 app_access_token（应用商店应用）
                https://open.feishu.cn/document/ukTMukTMukTM/uEjNz4SM2MjLxYzM
            获取 tenant_access_token（企业自建应用）
                https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM
            获取 tenant_access_token（应用商店应用）
                https://open.feishu.cn/document/ukTMukTMukTM/uMjNz4yM2MjLzYzM

        :return: 返回的 JSON 数据包
        """
        auth_url_dict = {
            TOKEN_TYPE_APP_ACCESS_TOKEN_INTERNAL: 'auth/v3/app_access_token/internal/'
        }

        return self._http.post(
            url=self.get_url(auth_url_dict.get(token_type)),
            data={
                "app_id": app_id,
                "app_secret": app_secret
            }
        ).json()
