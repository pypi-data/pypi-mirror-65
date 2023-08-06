from .broker import *


__ALL__ = ["Agent"]


class Agent(object):
    def __init__(self, app_name: str, key_pair: key_pair_format) -> None:
        self.__aese = lambda v, __={}: self.__check() and (
            __.update({0: randb((RSA.import_key(key_pair["public_key"]).n.bit_length()//8)-42)}) or
            (EasyRSA(public_key=key_pair["public_key"]).encrypt(__[0]), AESCipher(__[0]).encrypt(v))
        )
        self.__aesd = lambda k, v: self.__check() and AESCipher(
            EasyRSA(private_key=key_pair["private_key"]).decrypt(k)
        ).decrypt(v)
        self.__hmac = lambda v: self.__check() and mac(key_pair["public_key"], v)
        self.__setk = lambda k, v: self.__check() and mac(sha512(k), v)
        self.__app_name = self.__hmac(app_name)

    @staticmethod
    def __check():
        import inspect
        if not inspect.stack()[2][1].replace("\\", ".").replace("/", ".").endswith("site-packages.credsafe.agent.py"):
            raise Exception("call outside Agent() is prohibited")
        return True

    def __encrypt(self, v: Any) -> str:
        self.__check()
        sk, v = self.__aese(jd(v))
        sk = b64e(sk)
        hash = self.__hmac(v)
        return f"{hash} {sk} {v}"

    def set(self, id: str, pw: str, k: str, v: Any) -> Any:
        Broker(app_name=self.__app_name, username=self.__hmac(id)).set(self.__setk(pw, k), self.__encrypt(v))
        return self

    def __decrypt(self, v: str) -> Any:
        self.__check()
        hash, sk, v = v.split(" ")
        if hash == self.__hmac(v):
            return jl(self.__aesd(b64d(sk), v))
        raise Exception("credentials are tampered due to different hmac")

    def get(self, id: str, pw: str, k: str) -> Any:
        return self.__decrypt(Broker(app_name=self.__app_name, username=self.__hmac(id)).get(self.__setk(pw, k)))

    def rm(self, id: str, pw: str, k: str) -> bool:
        return Broker(app_name=self.__app_name, username=self.__hmac(id)).rm(self.__hmac(k))

    def destroy(self, id: str, pw: str) -> bool:
        return Broker(app_name=self.__app_name, username=self.__hmac(id)).destroy()




