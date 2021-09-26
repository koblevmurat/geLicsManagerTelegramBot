# from os import read
import sqlite3 
from cryptography.fernet import Fernet

con = None
is_new_key = False

def get_encryption_key ():
    key_file = open("key.txt", "a+")
    key_file.seek(0)
    key = key_file.readline().strip()
    if not key:
        key = Fernet.generate_key()
        key_file.flush()
        key_file.write(key.decode())
        isNewKey = True
    return key


def get_db_connection():
    conn = sqlite3.connect('settings.db')
    return conn


def close_db_connection(conn, commit=True):
    conn.close()


def request_setting():
    telegram_bot_token = input("telegram_bot_token: ")
    utils_path = input("Utils file path: ").strip()
    root_password = input("Root password: ").strip()
    bitmobile_host = input("Bitmobile Host address: ").strip()
    fern = Fernet(get_encryption_key())
    root_password = fern.encrypt(root_password.encode())
    return {'telegram_bot_token': telegram_bot_token, 'utils_path': utils_path, 'root_password': root_password, 'bitmobile_host': bitmobile_host}


def init_settings(rewrite = False):
    fern = Fernet(get_encryption_key())
    rewrite = is_new_key
    is_set = False
    conn = get_db_connection()
    cur = conn.cursor()
    settings = None

    cur.execute('''CREATE TABLE IF NOT EXISTS Settings 
                    (telegramBotToken text,
                    UtilsPath text, 
                    rootPassword text,
                    bitmobileHost)''')
    for values in cur.execute('SELECT * FROM Settings LIMIT 1'):
        is_set = True
        settings = {'telegramBotToken': values[0], 'UtilsPath': values[1], 'rootPassword': fern.decrypt(values[2]).decode(), 'bitmobileHost':values[3] }

    if rewrite:
        is_set = False

    if not is_set:
        settings = request_setting()
        cur.execute('INSERT INTO Settings VALUES (:telegramBotToken, :UtilsPath, :rootPassword, :bitmobileHost)', settings)
        settings['rootPassword'] = fern.decrypt(settings['rootPassword']).decode()
    conn.commit()
    close_db_connection(conn)
    return settings
    

def testModule():    
    # conn = ConnDB()
    # cur = conn.cursor()
    # cur.execute('''DROP TABLE Settings''')
    # conn.commit()
    # Disconnect(conn)
    init_settings(True)
    # print(getEncryptionKey())


if __name__ == '__main__':
    testModule()



