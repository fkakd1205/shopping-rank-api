import base64
from Crypto import Random
from Crypto.Cipher import AES

class AES128Crypto:

    def __init__(self, encrypt_key):
        self.BS = AES.block_size
        # 암호화 키중 BS사이즈 자리만큼만 잘라서 쓴다.
        self.encrypt_key = encrypt_key[:self.BS].encode(encoding='utf-8', errors='strict')
        self.pad = lambda s: bytes(s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS), 'utf-8')
        self.unpad = lambda s: s[0:-ord(s[-1:])]

    def encrypt(self, raw):
        # enc password 체크
        try:
            self.check_enc_password_format(self.encrypt_key)
        except Exception as e:
            print(str(e))
            return

        raw = self.pad(raw)
        # initialization vector를 매번 랜덤으로 생성 한다.
        iv = Random.new().read(self.BS)
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, iv)

        # 암호화시 앞에 iv와 암호화 값을 붙여 인코딩 한다.
        # 디코딩시 앞에서 BS(block_size) 만금 잘라서 iv를 구하고, 이를 통해 복호화한다.
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)

        # encrypt 에서 작업한 것처럼 첫 (block_size=BS)만큼을 잘라 iv를 만들고, 그 뒤를 복호화 하고자 하는 메세지로 잘라 만든다.
        iv = enc[:self.BS]
        encrypted_msg = enc[self.BS:]
        cipher = AES.new(self.encrypt_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(encrypted_msg)).decode('utf-8')

    def check_enc_password_format(self, data):
        if(len(data) < AES.block_size):
            raise Exception("\n [Error] : Please enter a longer ENC_PASSWORD...\n")
