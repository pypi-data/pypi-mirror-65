from .broker import *


__ALL__ = ["Agent"]


class Agent(object):
    def __init__(self, app_name: str, key_pair: key_pair_format, aes_key: bytes, hmac_key: bytes) -> None:
        self.__hmac = lambda _: mac(_, hmac_key)
        self.__skey = lambda: bytes(randb(len(aes_key))[i] ^ aes_key[i] for i in range(len(aes_key)))
        self.__aese = lambda k, v: AESCipher(k).encrypt(v)
        self.__aesd = lambda k, v: AESCipher(
            EasyRSA(private_key=key_pair["private_key"]).decrypt(k)
        ).decrypt(v)
        self.__rsae = lambda k: EasyRSA(public_key=key_pair["public_key"]).encrypt(k)
        self.__app_name = self.__hmac(app_name)

    @staticmethod
    def __check():
        import inspect
        if not inspect.stack()[2][1].replace("\\", ".").replace("/", ".").endswith("site-packages.credsafe.agent.py"):
            raise Exception("call outside Agent() is prohibited")

    def __username(self, id, pw):
        self.__check()
        return self.__hmac(id)+self.__hmac(pw)

    def __encrypt(self, v: Any) -> str:
        self.__check()
        k = self.__skey()
        v = self.__aese(k, jd(v))
        k = self.__rsae(k)
        hash = self.__hmac(v)
        return f"{hash} {k} {v}"

    def set(self, id: str, pw: str, k: str, v: Any) -> Any:
        Broker(app_name=self.__app_name, username=self.__username(id, pw)).set(self.__hmac(k), self.__encrypt(v))
        return self

    def __decrypt(self, v: str) -> Any:
        self.__check()
        hash, k, v = v.split(" ")
        if hash == self.__hmac(v):
            return jl(self.__aesd(k, v))
        raise Exception("credentials are tampered due to different hmac")

    def get(self, id: str, pw: str, k: str) -> Any:
        return self.__decrypt(Broker(app_name=self.__app_name, username=self.__username(id, pw)).get(self.__hmac(k)))

    def rm(self, id: str, pw: str, k: str) -> bool:
        return Broker(app_name=self.__app_name, username=self.__username(id, pw)).rm(self.__hmac(k))

    def destroy(self, id: str, pw: str) -> bool:
        return Broker(app_name=self.__app_name, username=self.__username(id, pw)).destroy()




