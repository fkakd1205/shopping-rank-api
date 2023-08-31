from config.pycryptodome.PyCryptoDomeConfigSetting import PyCryptoDomeConfigSetting

print("\n#======== input config value ========#")
ENC_PASSWORD = input("[ENC_PASSWORD] : ")
DB_USER = input("[DB_USER] : ")
DB_PASSWORD = input("[DB_PASSWORD] : ")
DB_HOST = input("[DB_HOST] : ")
DB_DATABASE = input("[DB_DATABASE] : ")

print("\n#======== encrypted key ========#")
configSetting = PyCryptoDomeConfigSetting(ENC_PASSWORD)

print("[DB_USER]")
print(configSetting.encrypt(DB_USER))
print("[DB_PASSWORD]")
print(configSetting.encrypt(DB_PASSWORD))
print("[DB_HOST]")
print(configSetting.encrypt(DB_HOST))
print("[DB_DATABASE]")
print(configSetting.encrypt(DB_DATABASE))
print("\n")
