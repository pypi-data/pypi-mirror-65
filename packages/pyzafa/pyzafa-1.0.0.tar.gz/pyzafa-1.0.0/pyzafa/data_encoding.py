# -*- coding: utf-8 -*-
"""数据编码"""
import base64


def base64encode(string, encoding='utf-8'):
    """把一个unicode字符串编码成base64字符串"""
    if isinstance(string, str):
        string = string.encode(encoding)
    return base64.b64encode(string).decode(encoding)


def base64decode(string, encoding='utf-8'):
    """把一个base64字符串解码生unicode字符串"""
    if isinstance(string, str):
        string = string.encode(encoding)
    return base64.b64decode(string).decode(encoding)
