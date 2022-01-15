from sys import path
path.append("../")

from Crypto.Cipher.AES import block_size
from set3.challenge2 import encrypt_AES_CTR, decrypt_AES_CTR
from base64 import b64decode
from Crypto.Random import get_random_bytes
from set1.challenge3 import xor_bytes, get_score
from string import printable

class Oracle:
	def __init__(self):
		self._key = get_random_bytes(16)
		self._IV = 0

	def encrypt(self, plaintext):
		return encrypt_AES_CTR(plaintext, self._key, self._IV)

# not perfect but you can understand most of the content
# The reason it isn't perfect is probably due to the fact that the way I assess how english a sentence is too primitive and needs to include capital letters and punctuations
def crack_CTR_auto(ciphertexts):
	max_len, ciphertext = max([(len(x), x) for x in ciphertexts])
	key = b''
	for i in range(max_len):
		column = b''
		for text in ciphertexts:
			column += bytes([text[i]]) if i < len(text) else b''
		score = -1
		curr_key = b''
		for p in printable.encode():
			predicted_key = xor_bytes(bytes([ciphertext[i]]), bytes([p]))
			curr_score = get_score(xor_bytes(column, predicted_key))
			if curr_score > score:
				score = curr_score
				curr_key = predicted_key
		key += curr_key

	for text in ciphertexts:
		print(xor_bytes(key[:len(text)], text))
	return

def crack_CTR_manual(ciphertexts):
	num_of_blocks = 0
	max_len, ciphertext = max([(len(x), x) for x in ciphertexts])
	previous_key = b''
	final_key = b''
	while True:
		if num_of_blocks == max_len // 16:
			return final_key
		prediction = input("Enter the predicted plaintext message for the largest plaintext, or press 'n' to predict the next block: ")
		if prediction == "n":
			num_of_blocks += 1
			final_key += previous_key 
			continue

		prediction = prediction.encode().ljust(16, b'\x00')
		potential_key = xor_bytes(ciphertext[num_of_blocks * block_size: (num_of_blocks + 1) * block_size], prediction)
		for text in ciphertexts:
			print(xor_bytes(text[: (num_of_blocks + 1) * block_size], final_key + potential_key))
		previous_key = potential_key
def main():
	h = open('data/19.txt', 'r')
	oracle = Oracle()
	plaintexts = h.read().split()
	ciphertexts = []
	for plaintext in plaintexts:
		ciphertexts.append(oracle.encrypt(b64decode(plaintext)))
	crack_CTR_auto(ciphertexts)
if __name__ == "__main__":
	main()
