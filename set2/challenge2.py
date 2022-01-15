from sys import path
path.append("../")

from Crypto.Cipher import AES
from base64 import b64decode
from set1.challenge7 import decrypt_AES_ECB
from set1.challenge3 import xor_bytes
from set2.challenge1 import pad_pkcs7, unpad_pkcs7

def encrypt_AES_ECB(plain_text, key):
	cipher = AES.new(key, AES.MODE_ECB)
	cipher_text = cipher.encrypt(plain_text)
	return cipher_text

def encrypt_AES_CBC(plain_text, key, IV):
	if len(plain_text) == 0:
		raise Exception("The plaintext is of 0 length")
	blocks = [plain_text[i * AES.block_size: i * AES.block_size + AES.block_size] for i in range(len(plain_text)//AES.block_size)]
	cipher_text_blocks = [encrypt_AES_ECB(xor_bytes(blocks[0], IV), key)]
	for i in range(len(blocks) - 1):
		cipher_text_blocks.append(encrypt_AES_ECB(xor_bytes(cipher_text_blocks[i], blocks[i + 1]), key))	
	return b''.join(cipher_text_blocks)

def decrypt_AES_CBC(cipher_text, key, IV):
	if len(cipher_text) == 0:
		raise Exception("The ciphertext is of length 0")
	xor_plain_text = decrypt_AES_ECB(cipher_text, key)
	cipher_text_blocks = [cipher_text[i * AES.block_size: i * AES.block_size + AES.block_size] for i in range(len(cipher_text)//AES.block_size)]
	xor_blocks = [decrypt_AES_ECB(block, key) for block in cipher_text_blocks]
	plain_text_blocks = [xor_bytes(xor_blocks[0], IV)]
	for i in range(len(xor_blocks) - 1):
		plain_text_blocks.append(xor_bytes(xor_blocks[i + 1], cipher_text_blocks[i]))
	return b"".join(plain_text_blocks)
	
def main():
	h = open('data/10.txt', 'r')
	data = b64decode(h.read())
	IV = bytes(16)
	key = b"YELLOW SUBMARINE"
	print(decrypt_AES_CBC(data, key, IV).decode('utf8'))
if __name__ == "__main__":
	main()
