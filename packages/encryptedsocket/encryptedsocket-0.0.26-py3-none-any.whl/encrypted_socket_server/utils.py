from aes_cipher import *
import hmac
import hashlib
import json
import pickle


__ALL__ = ["encrypt", "decrypt"]


def encrypt(key: str_or_bytes, plaintext: str_or_bytes) -> bytes:
    plaintext = AESCipher(key).encrypt(plaintext)
    hash = hmac.new(key.encode(), plaintext.encode(), hashlib.sha3_512).hexdigest()
    return f"{hash} {plaintext}".encode()


def decrypt(key: str_or_bytes, ciphertext: str) -> Any:
    mac, ciphertext = ciphertext.split(" ")
    hash = hmac.new(key.encode(), ciphertext.encode(), hashlib.sha3_512).hexdigest()
    if hash == mac:
        ciphertext = AESCipher(key).decrypt(ciphertext)
        try:
            return json.loads(ciphertext)
        except:
            return pickle.loads(ciphertext)
    else:
        raise Exception("current connection might be spoofed due to different hmac.")

