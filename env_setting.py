from config.pycryptodome.AES128Crypto import AES128Crypto

print("\n#======== Input config value ========#")
ENC_PASSWORD = input("[ENC_PASSWORD] : ")
DB_USER = input("[DB_USER] : ")
DB_PASSWORD = input("[DB_PASSWORD] : ")
DB_HOST = input("[DB_HOST] : ")
DB_DATABASE = input("[DB_DATABASE] : ")

print("\n#======== Copy and paste The following results into (.env) file. ========#\n")
configSetting = AES128Crypto(ENC_PASSWORD)

print("[DB_USER] : " + configSetting.encrypt(DB_USER))
print("[DB_PASSWORD] : " + configSetting.encrypt(DB_PASSWORD))
print("[DB_HOST] : " + configSetting.encrypt(DB_HOST))
print("[DB_DATABASE] : " + configSetting.encrypt(DB_DATABASE))
print("\n")
