# by Joao DaSilvaMarly

from passlib.hash import sha256_crypt
import binascii, os


def generate_token(half_size):
    return binascii.b2a_hex(os.urandom(half_size))

def hash_password(password):
    return sha256_crypt.encrypt(password)

def verify_hash(login_password, user_password):
    return sha256_crypt.verify(login_password, user_password)


# def print attributes with arg* when POST or GET
# refactoring of duplicated code
