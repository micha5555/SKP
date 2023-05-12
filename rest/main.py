from app import app
from app.db import createDb, deleteDB
from keys.generateKeys import generateKeys
import sys
from config import Dev_Config, Prod_Config

def message():
    print("""Podaj tryb uruchamiana programu:
        -p : produkcja
        -d : development
        -db-c : create database
        -db-d : delete database
        -keys-g : generate new ssl keys
        """)
    exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        message()

    context = ('keys/apiCert.crt', 'keys/apiPrivateKey.key')
    mode = sys.argv[1]

    if mode == '-p':
        app.config.from_object(Prod_Config)
        app.run(ssl_context=context, host='0.0.0.0', debug=False)
    elif mode == '-d':
        app.config.from_object(Dev_Config)
        app.run(ssl_context=context, host='0.0.0.0', debug=True)
    elif mode == '-db-c':
        with app.app_context():
            createDb()
    elif mode == '-db-d':
        with app.app_context():
            deleteDB()
    elif mode == '-keys-g':
        generateKeys()
    else:
        message()
    exit()