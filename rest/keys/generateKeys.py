from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta

def generateKeys():
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Mazowieckie"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Warszawa"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"SKP"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"Web&API"),
    ])

    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
        private_key.public_key()
    ).serial_number(x509.random_serial_number()).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(private_key, hashes.SHA256())

    # Save the private key to a file
    with open("keys/apiPrivateKey.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the certificate to a file
    with open("keys/apiCert.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))