import subprocess

def generate_self_signed_certificate(cert_file, key_file):
    subprocess.run(['openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '365', '-nodes', '-x509',
                    '-subj', '/C=US/ST=State/L=City/O=Organization/CN=localhost',
                    '-keyout', key_file, '-out', cert_file])
