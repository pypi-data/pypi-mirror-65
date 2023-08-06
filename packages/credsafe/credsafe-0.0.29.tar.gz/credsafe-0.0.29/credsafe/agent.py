from .broker import *


__ALL__ = ["Agent"]


class Agent(object):
    def __init__(self, app_name: str, key_pair: key_pair_format) -> None:
        __ = {}
        self.__aese = lambda v: self.__check() and (
                __.update({0: randb((RSA.import_key(key_pair["public_key"]).n.bit_length()//8)-42)}) or
                (__[0], AESCipher(EasyRSA(public_key=key_pair["public_key"]).encrypt(__[0])).encrypt(v))
        )
        self.__aesd = lambda k, v: self.__check() and AESCipher(
            EasyRSA(private_key=key_pair["private_key"]).decrypt(k)
        ).decrypt(v)
        self.__app_name = mac(key_pair["public_key"], app_name)

    @staticmethod
    def __check():
        import inspect
        if not inspect.stack()[2][1].replace("\\", ".").replace("/", ".").endswith("site-packages.credsafe.agent.py"):
            raise Exception("call outside Agent() is prohibited")
        return True

    def __encrypt(self, k: str, v: Any) -> str:
        self.__check()
        sk, v = self.__aese(jd(v))
        hash = mac(k, v)
        return f"{hash} {sk} {v}"

    def set(self, id: str, pw: str, k: str, v: Any) -> Any:
        Broker(app_name=self.__app_name, username=mac(pw, id)).set(mac(pw, k), self.__encrypt(pw, v))
        return self

    def __decrypt(self, k: str, v: str) -> Any:
        self.__check()
        hash, sk, v = v.split(" ")
        if hash == mac(k, v):
            return jl(self.__aesd(b64d(sk), v))
        raise Exception("credentials are tampered due to different hmac")

    def get(self, id: str, pw: str, k: str) -> Any:
        return self.__decrypt(pw, Broker(app_name=self.__app_name, username=mac(pw, id)).get(mac(pw, k)))

    def rm(self, id: str, pw: str, k: str) -> bool:
        return Broker(app_name=self.__app_name, username=mac(pw, id)).rm(mac(pw, k))

    def destroy(self, id: str, pw: str) -> bool:
        return Broker(app_name=self.__app_name, username=mac(pw, id)).destroy()




