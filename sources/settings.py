# from os import read
import sqlite3 
from cryptography.fernet import Fernet

con = None
isNewKey = False

def getEncryptionKey ():
    keyFile = open("key.txt","a+")
    keyFile.seek(0)
    key = keyFile.readline().strip() #.strip().encode()
    if not key:
        key = Fernet.generate_key()
        keyFile.flush()
        keyFile.write(key.decode())
        isNewKey = True
    return key

def ConnDB():       
    conn = sqlite3.connect('settings.db')
    return conn

def Disconnect(conn, Commit = True):
    conn.close()

def requestSetting():
    telegramBotToken = input("telegramBotToken: ")
    UtilsPath = input("Utils file path: ").strip()
    rootPassword = input("Root password: ").strip()
    bitmobileHost = input("Bitmobile Host address: ").strip()
    fern = Fernet(getEncryptionKey())
    rootPassword = fern.encrypt(rootPassword.encode())
    return {'telegramBotToken': telegramBotToken, 'UtilsPath': UtilsPath, 'rootPassword': rootPassword, 'bitmobileHost': bitmobileHost}

def InitSettings(rewrite = False):
    fern = Fernet(getEncryptionKey())   
    rewrite = isNewKey 
    isSet = False
    conn = ConnDB()
    cur = conn.cursor()        
    cur.execute('''CREATE TABLE IF NOT EXISTS Settings 
                    (telegramBotToken text,
                    UtilsPath text, 
                    rootPassword text,
                    bitmobileHost)''')
    for vals in cur.execute('SELECT * FROM Settings LIMIT 1'):
        isSet = True        
        Setting = {'telegramBotToken': vals[0], 'UtilsPath': vals[1], 'rootPassword': fern.decrypt(vals[2]).decode(), 'bitmobileHost':vals[3] }

    if rewrite:
        isSet = False

    if not isSet:
        Setting = requestSetting()
        cur.execute('INSERT INTO Settings VALUES (:telegramBotToken, :UtilsPath, :rootPassword, :bitmobileHost)', Setting)
        Setting['rootPassword'] = fern.decrypt(Setting['rootPassword']).decode()
    conn.commit()
    Disconnect(conn)
    return Setting
    

def testModule():    
    # conn = ConnDB()
    # cur = conn.cursor()
    # cur.execute('''DROP TABLE Settings''')
    # conn.commit()
    # Disconnect(conn)
    InitSettings(True)
    # print(getEncryptionKey())

if __name__ == '__main__':    
    testModule()



