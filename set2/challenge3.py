from sys import path
path.append("../")

from set1.challenge8 import number_of_repetitions_ECB
from set2.challenge2 import encrypt_AES_ECB, encrypt_AES_CBC
from Crypto.Cipher.AES import block_size
from Crypto import Random
from Crypto.Random import random 
from set2.challenge1 import pad_pkcs7

class AESOracle:
	@staticmethod
	def encrypt(plain_text):
		padded_plain_text = pad_pkcs7(AESOracle._add_random_padding(plain_text));
		key = Random.new().read(16)
		if random.randint(0, 1) == 1:
			return encrypt_AES_ECB(padded_plain_text, key), "ECB"
		IV = Random.new().read(16)
		return encrypt_AES_CBC(padded_plain_text, key, IV), "CBC"
	@staticmethod
	def _add_random_padding(text):
		return Random.get_random_bytes(random.randint(5, 10)) + text + Random.get_random_bytes(random.randint(5, 10))


def detect_cipher(cipher_text):
	if number_of_repetitions_ECB(cipher_text) > 0:
		return "ECB"
	return "CBC"

def main():
	data = bytes(64)
	oracle = AESOracle()

	for i in range(10000):
		(cipher_text, cipher) = oracle.encrypt(data)
		predicted_cipher = detect_cipher(cipher_text)
		if predicted_cipher != cipher:
			print(str(i), cipher, predicted_cipher, str(number_of_repetitions_ECB(cipher_text)))
			print(cipher_text)
			raise Exception("The prediction is wrong")
			quit()
	print("All 10000 guesses are correct :)") 
if __name__ == "__main__":
	main()
