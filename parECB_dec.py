import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES


def xor64(a, b):
    block = bytearray(a)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return bytes(block)


def init(shared_data, output_data, block_size, key):
    multiprocessing.shared_data = shared_data
    multiprocessing.output_data = output_data
    multiprocessing.block_size = block_size
    multiprocessing.key = key


def decrypt_block(cipher, counter, block_bytes):
    counter_bytes = counter.to_bytes(8, byteorder='big')
    encrypted_counter = cipher.encrypt(counter_bytes)
    res = xor64(encrypted_counter, block_bytes)
    return res


def mapper(blocks):
    cipher_text = multiprocessing.shared_data
    plain_text = multiprocessing.output_data
    block_size = multiprocessing.block_size
    key = multiprocessing.key
    cipher = DES.new(key, DES.MODE_ECB)

    counter = 0

    for i in blocks:
        offset = i * block_size
        block = cipher_text[offset:offset + block_size]
        decrypted = decrypt_block(cipher, counter, block)
        plain_text[offset:offset + block_size] = decrypted
        counter += 1
    return i


    
def rundec():
    key = b"haslo123"
    block_size = 8
    cipher_text = open("ciphertext", "rb").read()
    no_blocks = int(len(cipher_text) / block_size)
    W = 4

    shared_data = multiprocessing.RawArray(ctypes.c_ubyte, cipher_text)
    output_data = multiprocessing.RawArray(ctypes.c_ubyte, cipher_text)
    blocks = [range(i, no_blocks, W) for i in range(W)]
    pool = multiprocessing.Pool(W, initializer=init, initargs=(shared_data, output_data, block_size, key))
    starttime = time.time()
    pool.map(mapper, blocks)
    print('CTR Decrypt time parallel: ', (time.time() - starttime))
    decrypted = bytes(output_data)
    print('...', decrypted[-15:-1])

if __name__ == '__main__':
    rundec()