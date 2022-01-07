from sys import path
path.append("../")

from base64 import b64decode
from Crypto import Random
from set1.challenge8 import number_of_repetitions_ECB
from string import printable
from set2.challenge2 import encrypt_AES_ECB
rand_key = Random.get_random_bytes(16)

class ECBOracle:

	@staticmethod
	def encrypt(plain_text):
		data = plain_text + b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
		return encrypt_AES_ECB(data, rand_key)

def find_block_size(oracle):
	input_bytes = b""
	beginning_length = len(oracle.encrypt(input_bytes))
	while True:
		input_bytes += b"A"
		current_length = len(oracle.encrypt(input_bytes))
		if current_length > beginning_length:
			return current_length - beginning_length

def find_secret_text_size(oracle):
	input_bytes = b""
	beginning_length = len(oracle.encrypt(input_bytes))
	while True:
		input_bytes += b"A"
		current_length = len(oracle.encrypt(input_bytes))
		if current_length > beginning_length:
			return beginning_length + 1 - len(input_bytes) # Because beginning_length + 1 = len(input_bytes) + len(secret_text) 

def check_if_ECB(oracle):
	cipher_text = oracle.encrypt(bytes(64))
	if number_of_repetitions_ECB(cipher_text) > 0:
		return True
	return False

def crack_ECB(oracle, length, block_size):
	known_bytes = b"A" * (block_size - 1)
	alpha = bytes(printable, 'utf8')
	found_bytes = b""
	answer = b""
	for i in range(length):
		known_bytes = b"A" * (block_size - 1 - (i % block_size))
		cipher_text = oracle.encrypt(known_bytes)
		original_block = cipher_text[block_size * (i//block_size):(1 + i//block_size) * block_size]
		for char in alpha:
			if i//block_size == 0:
				possible_cipher_text = oracle.encrypt(known_bytes + found_bytes[-1 * (block_size - 1 - len(known_bytes)):] + bytes([char]))
			else:
				possible_cipher_text = oracle.encrypt(found_bytes[-1 * (block_size - 1):] + bytes([char]))
			prediction_block = possible_cipher_text[:block_size]
			if prediction_block == original_block:
				found_bytes += bytes([char])	
				known_bytes = known_bytes[1:]
				break
	return found_bytes

def main():
	oracle = ECBOracle()
	block_size = find_block_size(oracle)
	secret_length = find_secret_text_size(oracle)
	is_ECB = check_if_ECB(oracle)
	if is_ECB:
		secret = crack_ECB(oracle, secret_length, block_size)	
		print(secret.decode('utf8'))
	
if __name__ == "__main__":
	main()
