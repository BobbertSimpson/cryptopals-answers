from sys import path
path.append("../")

from set2.challenge2 import encrypt_AES_CBC, decrypt_AES_CBC
from Crypto.Random import random
from base64 import b64decode
from set2.challenge1 import unpad_pkcs7, pad_pkcs7
from Crypto import Random
from Crypto.Cipher.AES import block_size

class Oracle:
	def __init__(self, file):
		self._key = Random.get_random_bytes(16)
		self.IV = Random.get_random_bytes(16)
		self._texts = [b64decode(line) for line in file.read().split()]
	def encrypt(self):
		text = pad_pkcs7(random.choice(self._texts))
		cipher_text = encrypt_AES_CBC(text, self._key, self.IV)
		return cipher_text

	def padding_is_valid(self, cipher_text, iv):
		text = decrypt_AES_CBC(cipher_text, self._key, iv)
		try:
			unpad_pkcs7(text)
			return True
		except:
			return False

def find_iv(iv, guessed_byte, plain_text):
	padding_length = len(plain_text) + 1
	index_of_element = len(iv) - padding_length
	plain_text = bytes([guessed_byte]) + plain_text
	new_iv = iv[:index_of_element]
	for i in range(padding_length):
		element = bytes([iv[i + index_of_element] ^ padding_length ^ plain_text[i]]) # if we xor it with the iv and the correctly guessed byte it will zero out, and then we can xor it with the padding number that we want 
		new_iv += element
	return bytes(new_iv)

def crack_block(oracle, block, iv):
	plain_text = b''
	for j in range(len(iv) - 1, -1, -1):	
		found = []
		for k in range(256):
			current_iv = find_iv(iv, k, plain_text)
			if oracle.padding_is_valid(block, current_iv):
				found.append(bytes([k]))
		while len(found) != 1:
			for byte in found:
				for k in range(256):
					current_iv = find_iv(iv, k, byte + plain_text)
					if oracle.padding_is_valid(block, current_iv):
						found = [byte]
						break;
		plain_text = found[0] + plain_text
	return plain_text

def crack_CBC(oracle, cipher_text):
	answer = b''
	cipher = bytearray(oracle.IV + cipher_text)
	cipher_blocks = [cipher[l * block_size: (l + 1) * block_size] for l in range(len(cipher)//block_size)]
	for i in range(len(cipher_blocks) - 1):
		current_iv = cipher_blocks[i]
		block = cipher_blocks[i + 1]
		found_block = crack_block(oracle, block, current_iv)
		answer += found_block
	answer = unpad_pkcs7(answer)
	print(answer)
	return answer
def main():
	file = open('data/17.txt' ,'r')
	oracle = Oracle(file)
	cipher_text = oracle.encrypt()
	answer = crack_CBC(oracle, cipher_text)

if __name__ == "__main__":
	main()

