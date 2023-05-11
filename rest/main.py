from app import app
from app.db import createDb, deleteDB
import sys

def message():
    print("""Podaj tryb uruchamiana programu:
        -p : produkcja
        -d : development
        -db-c : create database
        -db-d : delete database
        """)
    exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        message()

    context = ('keys/apiCert.crt', 'keys/apiPrivateKey.key')
    mode = sys.argv[1]

    if mode == '-p':
        app.run(ssl_context=context, host='0.0.0.0', debug=False)
    elif mode == '-d':
        app.run(ssl_context=context, host='0.0.0.0', debug=True)
    elif mode == '-db-c':
        with app.app_context():
            createDb()
    elif mode == '-db-d':
        with app.app_context():
            deleteDB()
    else:
        message()