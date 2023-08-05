from cryptography.fernet import Fernet
from environs import Env


env = Env()
env.read_env(override=True)

CRYPT_KEY = env.str('CRYPT_KEY', b'zsWqnSYZ9eoocR0mQhbZN_U2Ed7zZ4zINTGTU3rbfaQ=')


def decrypt_emails_list(d_emails_list) -> list:
    fernet = Fernet(CRYPT_KEY)
    return [fernet.decrypt(email).decode() for email in d_emails_list]
