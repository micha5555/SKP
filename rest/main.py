import sys
from config import Config, DBConfig

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
        Config.SQLALCHEMY_DATABASE_URI = DBConfig.SQLALCHEMY_DATABASE_URI_PROD
        from app import app
        app.run(ssl_context=context, host='0.0.0.0', debug=False)
    elif mode == '-d':
        Config.SQLALCHEMY_DATABASE_URI = DBConfig.SQLALCHEMY_DATABASE_URI_DEV
        from app import app
        app.run(ssl_context=context, host='0.0.0.0', debug=True)
    elif mode == '-db-c':
        from app.db import createDb
        from app import app
        with app.app_context():
            createDb()
    elif mode == '-db-d':
        from app.db import deleteDB
        from app import app
        with app.app_context():
            deleteDB()
    elif mode == '-keys-g':
        from keys.generateKeys import generateKeys
        generateKeys()
    else:
        message()
    exit()