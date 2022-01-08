from sys import path
path.append("../")

from challenge2 import encrypt_AES_CBC, decrypt_AES_CBC
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher.AES import block_size

class Oracle:
	def __init__(self):
		self._key = Random.get_random_bytes(AES.key_size[0])
		self._IV = Random.get_random_bytes(block_size)
		self._prefix = b"comment1=cooking%20MCs;userdata="
		self._suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
	def encrypt(self, data):
		padded_data = self._prefix + data.decode().replace(';', '').replace('=', '').encode() + self._suffix
		return encrypt_AES_CBC(padded_data, self._key, self._IV)
	def check_admin(self, cipher_text):
		data = decrypt_AES_CBC(cipher_text, self._key, self._IV)
		return b";admin=true;" in data
	def decrypt(self, cipher_text):
		return decrypt_AES_CBC(cipher_text, self._key, self._IV)
def bitflip_CBC():
	#We assume that we know the size of the prefix and the block_size (16) but we could have found them out using functions that are similar to the ones used in the pervious challenges
	injection = b":admin<true" # We use ':' and < as both of them are one off from the desired characters
	input_bytes = b"A" * (block_size * 2 - len(injection)) + injection #The first block of As is in order not to ruin the prefix bytes
	oracle = Oracle()
	cipher_text = bytearray(oracle.encrypt(input_bytes))
	cipher_text[block_size * 3 - len(injection)] ^= 1
	cipher_text[block_size * 3 - 5] ^= 1
	print(len(cipher_text))
	admin = oracle.decrypt(bytes(cipher_text))
	print(admin)
	print(oracle.check_admin(cipher_text))
def main():
	bitflip_CBC()

if __name__ == "__main__":
	main()
