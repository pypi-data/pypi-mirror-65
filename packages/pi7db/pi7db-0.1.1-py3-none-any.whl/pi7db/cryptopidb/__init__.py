from Crypto import Random
import base64
from Crypto.Cipher import AES
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def genkey(password_provided):
  password = password_provided.encode()
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=16,
    salt=password,
    iterations=100000,
    backend=default_backend()
  )
  key = base64.urlsafe_b64encode(kdf.derive(password))
  return key
  
def pad(s):
    return s + "\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key,data):
    enc = encrypt(data, key)
    with open(file_name+'.pi7db', 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name+'.pi7db', 'rb') as fo:
        ciphertext = fo.read()
    decdata = decrypt(ciphertext, key)
    return decdata.decode('UTF-8')

