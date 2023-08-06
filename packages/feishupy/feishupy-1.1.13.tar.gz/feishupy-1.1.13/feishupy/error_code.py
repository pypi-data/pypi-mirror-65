# -*- coding: utf-8 -*-
from enum import IntEnum, unique


@unique
class APIErrorCode(IntEnum):
    """错误码

    https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uMDOyUjLzgjM14yM4ITN
    """
    # page token 格式非法
    PAGE_TOKEN_INVALID = 100001

    # fields 中存在非法字段名
    INVALID_FIELD_SELECTION = 100002

    # 时间格式未遵循 RFC3339 标准
    TIME_FORMAT_MUST_FOLLOW_RFC3339_STANDARD = 100003

    # building ID 非法
    BUILDING_ID_INVALID = 100004

    # room ID 非法
    ROOM_ID_INVALID = 100005

    # 内部错误
    INTERNAL_ERROR = 105001
