import socket
import json
import pickle
import random
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
            self.b = random.randint(10**2, 10**3)
            self.g = ingredients["g"]
            self.p = ingredients["p"]
            self.akey = ingredients["akey"]
            self.bkey = pow(self.g, self.b, self.p)
            self.request("set_bkey", self.bkey)
            self.key = str(pow(self.akey, self.b, self.p))

    def request(self, command: str, data: Any = None) -> Any:
        request = dict(command=command, data=data)
        try:
            request = json.dumps(request).encode()
        except:
            request = pickle.dumps(request)
        if self.encrypted and self.key:
            request = encrypt(self.key, request)
        self.s.send(request)
        while True:
            response = self.s.recv(1024*4).decode()
            if response:
                if self.encrypted and self.key:
                    return decrypt(self.key, response)
                else:
                    return json.loads(response)


