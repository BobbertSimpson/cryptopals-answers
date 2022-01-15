from sys import path
path.append("../")

from base64 import b64decode
from Crypto import Random
from set1.challenge8 import number_of_repetitions_ECB
from string import printable
from set2.challenge2 import encrypt_AES_ECB
from set2.challenge1 import pad_pkcs7
from Crypto.Random import random

rand_key = Random.get_random_bytes(16)
rand_prefix = Random.get_random_bytes(random.randint(0, 256))

class ECBOracle:

	@staticmethod
	def encrypt(plain_text):
		data = pad_pkcs7(rand_prefix + plain_text + b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))
		return encrypt_AES_ECB(data, rand_key)

def find_block_size(oracle):
	input_bytes = b""
	beginning_length = len(oracle.encrypt(input_bytes))
	while True:
		input_bytes += b"A"
		current_length = len(oracle.encrypt(input_bytes))
		if current_length > beginning_length:
			return current_length - beginning_length

def find_secret_text_size(oracle, prefix_length):
	input_bytes = b""
	beginning_length = len(oracle.encrypt(input_bytes))
	while True:
		input_bytes += b"A"
		current_length = len(oracle.encrypt(input_bytes))
		if current_length > beginning_length:
			return beginning_length + 1 - len(input_bytes) - prefix_length # Because beginning_length + 1 = len(prefix) + len(input_bytes) + len(secret_text) 

def find_index_of_repetition(text, block_size):
	array = [text[i * block_size: (i + 1) * block_size] for i in range(len(text) // block_size)]
	for i in range(len(array) - 1):
		if array[i] == array[i + 1]:
			return i
	return -1

def find_prefix_size(oracle, block_size):
	input_bytes = b"A" * (block_size * 2 - 1)
	cipher_text = oracle.encrypt(input_bytes)
	while find_index_of_repetition(cipher_text, block_size) == -1:
		input_bytes += b"A"
		cipher_text = oracle.encrypt(input_bytes)
	index_of_repetition = find_index_of_repetition(cipher_text, block_size) * block_size
	l = len(cipher_text[:index_of_repetition]) - (len(input_bytes) - 2 * block_size)
	return l


def check_if_ECB(oracle):
	cipher_text = oracle.encrypt(bytes(64))
	if number_of_repetitions_ECB(cipher_text) > 0:
		return True
	return False

def crack_ECB(oracle, prefix_length, secret_length, block_size):
	prefix_blocks_index = prefix_length//block_size + 1
	min_input = block_size * prefix_blocks_index - prefix_length
	alpha = bytes(printable, 'utf8')
	found_bytes = b""
	answer = b""
	for i in range(secret_length):
		known_bytes = b"A" * (block_size - 1 - (i % block_size))
		cipher_text = oracle.encrypt(b"A" * min_input + known_bytes)
		original_block = cipher_text[block_size * (i//block_size + prefix_blocks_index):(1 + i//block_size + prefix_blocks_index) * block_size]
		for char in alpha:
			if i//block_size == 0:
				possible_cipher_text = oracle.encrypt(b"A" * min_input + known_bytes + found_bytes[-1 * (block_size - 1 - len(known_bytes)):] + bytes([char]))
			else:
				possible_cipher_text = oracle.encrypt(b"A" * min_input + found_bytes[-1 * (block_size - 1):] + bytes([char]))
			prediction_block = possible_cipher_text[prefix_blocks_index * block_size:prefix_blocks_index * block_size + block_size]
			if prediction_block == original_block:
				found_bytes += bytes([char])	
				break
	return found_bytes

def main():
	oracle = ECBOracle()
	block_size = find_block_size(oracle)
	prefix_length = find_prefix_size(oracle, block_size)
	secret_length = find_secret_text_size(oracle, prefix_length)
	
	is_ECB = check_if_ECB(oracle)
	if is_ECB:
		secret = crack_ECB(oracle, prefix_length, secret_length, block_size)	
		print(secret.decode('utf8'))
	
if __name__ == "__main__":
	main()
