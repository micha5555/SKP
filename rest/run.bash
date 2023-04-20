export FLASK_APP=app
export FLASK_DEBUG=true
flask run --cert=apiCert.crt --key=apiPrivateKey.key --host=0.0.0.0 
