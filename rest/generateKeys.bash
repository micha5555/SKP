openssl genrsa -aes256 -out apiPrivateKey.key
openssl req -new -x509 -days 365 -key apiPrivateKey.key -out apiCert.crt
