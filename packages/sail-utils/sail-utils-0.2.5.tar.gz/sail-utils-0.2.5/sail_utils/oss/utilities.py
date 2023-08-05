# -*- coding: utf-8 -*-
"""
oss utilities module
"""

from io import BytesIO
from typing import List

import oss2
from sail_utils import LOGGER


class OSSUtility:
    """
    class for connect with aliyun oss
    """

    def __init__(self,
                 access_key_id: str,
                 access_key_secret: str,
                 bucket: str,
                 endpoint: str):
        self._bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret),
                                   endpoint,
                                   bucket)

    def put_binary(self, key: str, buffer: bytes):
        """
        put a binary file to aliyun oss
        :param key:
        :param buffer:
        :return:
        """
        with BytesIO(buffer) as writer:
            self._bucket.put_object(key, writer)
        LOGGER.info(f"saved file: <{key}>")

    def put_text(self, key: str, text: str):
        """
        put a plain text file to aliyun oss
        :param key:
        :param text:
        :return:
        """
        self._bucket.put_object(key, text)
        LOGGER.info(f"saved file: <{key}>")

    def get_object(self, key: str) -> bytes:
        """
        get file object from oss
        :param key:
        :return:
        """
        result = self._bucket.get_object(key)
        return b"".join(chunk for chunk in result)

    def list(self, prefix: str) -> List[str]:
        """
        list all the files under this folder
        :param prefix:
        :return:
        """
        is_truncated = True
        next_marker = ''
        while is_truncated:
            results = self._bucket.list_objects(prefix=prefix,
                                                marker=next_marker,
                                                max_keys=1000)
            is_truncated = results.is_truncated
            next_marker = results.next_marker
            for result in results.object_list:
                yield result.key
