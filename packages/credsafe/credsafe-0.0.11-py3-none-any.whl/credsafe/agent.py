from .broker import *


__ALL__ = ["Agent"]


class Agent(object):
    def __init__(self, app_name: str, key_pair: key_pair_format, hmac_key: bytes) -> None:
        self.__hmac_key = hmac_key
        self.__app_name = mac(app_name, self.__hmac_key)
        self.__key_pair = key_pair

    def __encrypt(self, v: Any) -> str:
        v = b64e(EasyRSA(public_key=self.__key_pair["public_key"]).encrypt(jd(v)))
        hash = mac(v, self.__hmac_key)
        return f"{hash} {v}"

    def set(self, id: str, pw: str, k: str, v: Any) -> Any:
        Broker(app_name=self.__app_name, username=mac(id, self.__hmac_key)+mac(pw, self.__hmac_key))\
            .set(mac(k, self.__hmac_key), self.__encrypt(v))
        return self

    def __decrypt(self, v: str) -> Any:
        hash, v = v.split(" ")
        if hash == mac(v, self.__hmac_key):
            return jl(EasyRSA(private_key=self.__key_pair["private_key"]).decrypt(b64d(v)))
        raise Exception("credentials are tampered due to different hmac")

    def get(self, id: str, pw: str, k: str) -> Any:
        return self.__decrypt(
            Broker(app_name=self.__app_name, username=mac(id, self.__hmac_key)+mac(pw, self.__hmac_key))
            .get(mac(k, self.__hmac_key)))





