import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# zakłada, że a i b są bytes
def xor64(a, b):
    block = bytearray(a)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return bytes(block)

# zakłada, że key i plain_text są bytes
def encrypt_ECB_serial(key, plain_text, no_blocks, block_size):
    cipher_text = bytearray(plain_text) # kopia! bytes -> bytearray
    des = DES.new(key, DES.MODE_ECB)
    for i in range(no_blocks):
        offset = i*block_size
        block = plain_text[offset:offset+block_size]
        encrypted = des.encrypt(block)
        cipher_text[offset:offset+block_size] = encrypted
    return bytes(cipher_text) # bytearray -> bytes   

# zakłada, że key i cipher_text są bytes
def decrypt_ECB_serial(key, cipher_text, no_blocks, block_size):
    plain_text = bytearray(cipher_text)
    des = DES.new(key, DES.MODE_ECB)
    for i in range(no_blocks):
        offset = i*block_size
        block = cipher_text[offset:offset+block_size]
        decrypted = des.decrypt(block)
        plain_text[offset:offset+block_size] = decrypted
    return bytes(plain_text)       

def runser():
    plain_text = b"alamakot"*100000
    key = b"haslo123"
    iv = get_random_bytes(8)
    block_size = 8
    no_blocks = int(len(plain_text)/block_size)
    
    starttime = time.time()
    cipher_text = encrypt_ECB_serial(key, plain_text, no_blocks, block_size)
    print('ECB Encrypt time serial: ', (time.time() - starttime))
    print('...', cipher_text[-15:-1])

    
    starttime = time.time()
    decrypted = decrypt_ECB_serial(key, cipher_text, no_blocks, block_size)
    print('ECB Decrypt time serial: ', (time.time() - starttime))
    print('...', decrypted[-15:-1])
    