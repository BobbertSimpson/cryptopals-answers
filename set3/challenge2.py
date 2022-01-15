from sys import path
path.append("../")

from struct import pack
from Crypto.Cipher.AES import block_size
from set2.challenge2 import encrypt_AES_ECB
from set1.challenge3 import xor_bytes
from base64 import b64decode

def encrypt_AES_CTR(plaintext, key, IV):
	if len(plaintext) % block_size == 0:
		num_blocks = len(plaintext)//block_size
	else:
		num_blocks = len(plaintext) // block_size + 1
	plaintext_blocks = [plaintext[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]
	counter = 0
	ciphertext = b''
	for block in plaintext_blocks:
		keystream = encrypt_AES_ECB(pack('<Q', IV) + pack('<Q', counter), key)
		ciphertext += xor_bytes(keystream[:len(block)], block)
		counter += 1
	return ciphertext

def decrypt_AES_CTR(ciphertext, key, IV):
	ciphertext_blocks = [ciphertext[i * block_size:(i + 1) * block_size] for i in range(len(ciphertext)//block_size)]
	counter = 0
	plaintext = b''
	for block in ciphertext_blocks:
		keystream = encrypt_AES_ECB(pack('<Q', IV) + pack('<Q', counter), key)
		plaintext += xor_bytes(keystream[:len(block)], block)
		counter += 1
	return plaintext

def main():
	ciphertext = b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
	plaintext = decrypt_AES_CTR(ciphertext, b"YELLOW SUBMARINE", 0)
	print(plaintext)

if __name__ == "__main__":
	main()
