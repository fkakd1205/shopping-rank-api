import os
from dotenv import load_dotenv
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

load_dotenv()

KEY_SALT = os.environ.get('KEY_SALT')
BYTE_SIZE = int(os.environ.get('KEY_SALT_BYTE_SIZE'))

class PyCryptoDomeUtils():

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, data):
        data = data.encode()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv())
        raw = pad(data, BYTE_SIZE)
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')
    
    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv())
            dec = cipher.decrypt(enc)
            return unpad(dec, BYTE_SIZE).decode('utf-8')
        except:
            print("configuration error")
        
    
    def iv(self):
        salt = KEY_SALT.zfill(BYTE_SIZE)[:BYTE_SIZE]
        return salt.encode('utf8')
