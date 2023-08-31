from enum import Enum
from Crypto.Cipher import AES

class AESAlgorithmModeEnum(Enum):
    ECB = AES.MODE_ECB
    CBC = AES.MODE_CBC
    CFB = AES.MODE_CFB
    OFB = AES.MODE_OFB
    CTR = AES.MODE_CTR
    OPENPGP = AES.MODE_OPENPGP
    CCM = AES.MODE_CCM
    EAX = AES.MODE_EAX
    SIV = AES.MODE_SIV
    GCM = AES.MODE_GCM
    OCB = AES.MODE_OCB
