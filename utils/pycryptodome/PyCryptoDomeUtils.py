import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BYTE_SIZE = 16

class PyCryptoDomeUtils():
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message, BYTE_SIZE)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')
    
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        dec = cipher.decrypt(enc)
        return unpad(dec, BYTE_SIZE).decode('utf-8')
    
    def __iv(self):
        return chr(0) * 16

