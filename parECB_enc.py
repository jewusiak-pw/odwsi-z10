import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

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

def encrypt_block(cipher, counter, block_bytes):
	counter_bytes = counter.to_bytes(8, byteorder='big')
	encrypted_counter = cipher.encrypt(counter_bytes)
	res = xor64(encrypted_counter, block_bytes)
	return res

def mapper(blocks):
	plain_text = multiprocessing.shared_data
	cipher_text  = multiprocessing.output_data
	block_size  = multiprocessing.block_size
	key = multiprocessing.key
	cipher = DES.new(key, DES.MODE_ECB)
		
	counter=0

	for i in blocks:
		offset = i * block_size
		block = plain_text[offset:offset + block_size]
		encrypted = encrypt_block(cipher, counter, block)
		cipher_text[offset:offset + block_size] = encrypted
		counter+=1
	return i


def runenc():
	key = b"haslo123"
	block_size = 8
	plain_text = b"alamakot"*100
	no_blocks = int(len(plain_text) / block_size)
	W = 4
	
	shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
	output_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
	blocks = [range(i, no_blocks, W) for i in range(W)]
	pool = multiprocessing.Pool(W, initializer=init, initargs=(shared_data, output_data, block_size, key))
	starttime = time.time()
	pool.map(mapper, blocks)
	print('CTR Encrypt time parallel: ', (time.time() - starttime))
	encrypted = bytes(output_data)
	open('ciphertext', "wb").write(encrypted)
	print('...', encrypted[-15:-1])

if __name__ == '__main__':
	runenc()