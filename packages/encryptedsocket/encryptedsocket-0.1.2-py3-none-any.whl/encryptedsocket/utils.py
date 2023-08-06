from aescipher import *
import hmac
import hashlib
import json
import pickle


__ALL__ = ["encrypt", "decrypt"]


def encrypt(key: str_or_bytes, plaintext: str_or_bytes) -> bytes:
    ciphertext = AESCipher(key).encrypt(plaintext)
    hash = mac(key, ciphertext)
    return f"{hash} {ciphertext}".encode("utf-8")


def decrypt(key: str_or_bytes, ciphertext: str) -> Any:
    mac, ciphertext = ciphertext.split(" ")
    hash = mac(key, ciphertext)
    if hash == mac:
        ciphertext = AESCipher(key).decrypt(ciphertext)
        try:
            return jl(ciphertext)
        except:
            return pickle.loads(ciphertext)
    else:
        raise Exception("current connection might be spoofed due to different hmac.")




