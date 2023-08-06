import keyring
import random
import json
import hmac
from base64 import b64decode, b64encode
import os
from easyrsa import EasyRSA
from omnitools import *


__ALL__ = ["Broker"]


class Broker(object):
    def __init__(self, app_name: str, username: str) -> None:
        self.split_length = 10**3
        self.__app_name = app_name
        self.__username = username
        if self.__get() == "":
            self.set("", "")

    def __get(self) -> str:
        import inspect
        if not inspect.stack()[1][1].replace("\\", ".").replace("/", ".").endswith("site-packages.credsafe.broker.py"):
            raise Exception("call to Broker._Broker__get() is prohibited")
        v = ""
        i = 0
        while True:
            _ = keyring.get_password(f"{self.__app_name}[{i}]", self.__username)
            if _ is None:
                return v
            else:
                v += _
                i += 1

    def __decrypt(self, v: str = None) -> dict:
        if v is None:
            v = self.__get()
            if v == "":
                return {}
        return json.loads(b64decode(v).decode("utf-8"))

    def get(self, k: str) -> str:
        return self.__decrypt()[k]

    def __set(self, k: str, v: str) -> dict:
        _ = self.__decrypt()
        _[k] = v
        return _

    def __encrypt(self, v: dict) -> str:
        return b64encode(json.dumps(v).encode("utf-8")).decode("utf-8")

    def set(self, k: str, v: str) -> True:
        v = self.__encrypt(self.__set(k, v))
        i = 0
        while v:
            keyring.set_password(f"{self.__app_name}[{i}]", self.__username, v[:self.split_length])
            v = v[self.split_length:]
            i += 1
        self.__delete(i)
        return True

    def __delete(self, i: int = 0) -> True:
        while True:
            kr = (f"{self.__app_name}[{i}]", self.__username)
            _ = keyring.get_password(*kr)
            if _ is None:
                return True
            else:
                keyring.delete_password(*kr)
                i += 1

    def destroy(self) -> None:
        self.__delete(0)
        self.__username = None



