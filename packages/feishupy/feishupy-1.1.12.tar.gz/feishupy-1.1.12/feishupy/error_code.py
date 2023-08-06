# -*- coding: utf-8 -*-
from enum import IntEnum, unique


@unique
class RESSTAPIErrorCode(IntEnum):
    """
    REST API 公共错误码，请参考 https://cloud.tencent.com/document/product/269/1519
    IM SDK 的错误码 + 服务端的错误码+ IM SDK V3 版本的错误码https://cloud.tencent.com/document/product/269/1671
    """
    # 请求包非法
    BODY_ILLEGAL_20001 = 20001

    # UserSig 或 A2 失效
    USER_SIG_OR_A2_INVALID_20002 = 20002

    # 消息发送方或接收方 UserID 无效或不存在，请检查 UserID 是否已导入即时通信 IM
    TO_ACCOUNT_OR_FROM_ACCOUNT_USER_ID_INVALID_20003 = 20003

    # 网络异常，请重试
    NETWORK_ERROR_20004 = 20004
