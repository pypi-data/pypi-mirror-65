import socket
import json
import pickle
from .utils import *


__ALL__ = ["SC"]


class SC(object):
    def __init__(self, host: str = "127.199.71.10", port: int = 39291, encrypted: bool = True) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, int(port)))
        self.encrypted = encrypted
        self.key = None
        if self.encrypted:
            ingredients = self.request("get_akey")
            b = randi()
            g = ingredients["g"]
            p = ingredients["p"]
            bkey = pow(g, b, p)
            self.request("set_bkey", bkey)
            self.key = str(pow(ingredients["akey"], b, p))

    def request(self, command: str, data: Any = None) -> Any:
        request = dict(command=command, data=data)
        try:
            request = utf8e(jd(request))
        except:
            request = pickle.dumps(request)
        if self.encrypted and self.key:
            request = encrypt(self.key, request)
        self.s.send(request)
        while True:
            response = utf8d(self.s.recv(1024*4))
            if response:
                if self.encrypted and self.key:
                    return decrypt(self.key, response)
                else:
                    return jl(response)


