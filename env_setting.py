from config.pycryptodome.AES128Crypto import AES128Crypto
import uuid

print("\n#======== Input config value ========#")
ENC_PASSWORD = input("[ENC_PASSWORD] : ")
DB_USER = input("[DB_USER] : ")
DB_PASSWORD = input("[DB_PASSWORD] : ")
DB_HOST = input("[DB_HOST] : ")
DB_DATABASE = input("[DB_DATABASE] : ")

print("\n")
SLAVE_DB_USER = input("[SLAVE_DB_USER] : ")
SLAVE_DB_PASSWORD = input("[SLAVE_DB_PASSWORD] : ")
SLAVE_DB_HOST = input("[SLAVE_DB_HOST] : ")
SLAVE_DB_DATABASE = input("[SLAVE_DB_DATABASE] : ")


print("\n#======== Copy and paste The following results into (.env) file. ========#\n")
configSetting = AES128Crypto(ENC_PASSWORD)

print("[DB_USER] : " + configSetting.encrypt(DB_USER))
print("[DB_PASSWORD] : " + configSetting.encrypt(DB_PASSWORD))
print("[DB_HOST] : " + configSetting.encrypt(DB_HOST))
print("[DB_DATABASE] : " + configSetting.encrypt(DB_DATABASE))

print("[SLAVE_DB_USER] : " + configSetting.encrypt(SLAVE_DB_USER))
print("[SLAVE_DB_PASSWORD] : " + configSetting.encrypt(SLAVE_DB_PASSWORD))
print("[SLAVE_DB_HOST] : " + configSetting.encrypt(SLAVE_DB_HOST))
print("[SLAVE_DB_DATABASE] : " + configSetting.encrypt(SLAVE_DB_DATABASE))

print("[NRANK_DIRECT_ACCESS_KEY] : " + str(uuid.uuid4()))
