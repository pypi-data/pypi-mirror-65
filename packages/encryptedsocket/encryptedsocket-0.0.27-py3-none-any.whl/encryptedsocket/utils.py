from aescipher import *
import hmac
import hashlib
import json
import pickle
import random


__ALL__ = ["encrypt", "decrypt", "randno"]


def encrypt(key: str_or_bytes, plaintext: str_or_bytes) -> bytes:
    plaintext = AESCipher(key).encrypt(plaintext)
    hash = hmac.new(key.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha3_512).hexdigest()
    return f"{hash} {plaintext}".encode("utf-8")


def decrypt(key: str_or_bytes, ciphertext: str) -> Any:
    mac, ciphertext = ciphertext.split(" ")
    hash = hmac.new(key.encode("utf-8"), ciphertext.encode("utf-8"), hashlib.sha3_512).hexdigest()
    if hash == mac:
        ciphertext = AESCipher(key).decrypt(ciphertext)
        try:
            return json.loads(ciphertext)
        except:
            return pickle.loads(ciphertext)
    else:
        raise Exception("current connection might be spoofed due to different hmac.")


def randno(power: int = 6) -> int:
    power = int(power)
    return random.randint(10 ** power, 10 ** (power + 1) - 1)


