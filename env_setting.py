from config.pycryptodome.PyCryptodomeConfigSetting import PyCryptodomeConfigSetting

print("\n#======== Input config value ========#")
ENC_PASSWORD = input("[ENC_PASSWORD] : ")
DB_USER = input("[DB_USER] : ")
DB_PASSWORD = input("[DB_PASSWORD] : ")
DB_HOST = input("[DB_HOST] : ")
DB_DATABASE = input("[DB_DATABASE] : ")
AES_ALGORITHM_MODE = input("[AES_MODE] (ex. ECB, CBC, CFB, OFB, CTR, etc.) : ")

print("\n#======== Copy and paste The following results into (.env) file. ========#\n")
configSetting = PyCryptodomeConfigSetting(ENC_PASSWORD, AES_ALGORITHM_MODE)

print("[DB_USER] : " + configSetting.encrypt(DB_USER))
print("[DB_PASSWORD] : " + configSetting.encrypt(DB_PASSWORD))
print("[DB_HOST] : " + configSetting.encrypt(DB_HOST))
print("[DB_DATABASE] : " + configSetting.encrypt(DB_DATABASE))
print("\n")
