from sys import path
path.append("../")

from base64 import b64decode
from set1.challenge7 import decrypt_AES_ECB
from set2.challenge2 import unpad_pkcs7
from Crypto.Random import get_random_bytes
from struct import pack
from Crypto.Cipher import AES

class CTR_oracle:
	def __init__(self):
		self._key = get_random_bytes(16)
		self._IV = get_random_bytes(16)

	def edit(self, ciphertext, offset, newtext):
		assert len(ciphertext) >= len(newtext) + offset
		start_block = offset//16
		end_block = (len(newtext) + offset)//16
		start_byte = offset % 16
		counter = start_block
		keystream = b''
		cipher = AES.new(self._key, AES.MODE_ECB)
		while counter < end_block + 1:
			keystream += cipher.encrypt(pack('<Q', self._IV) + pack('<Q', counter))
			counter += 1
		
		while counter < start_byte + (len(newtext) // 16) + 1:
			
		return ciphertext[:offset] + newciphertext + ciphertext[offset + len(newtext):]
		
	

def main():
	h = open('data/25.txt', 'r')
	plaintext = unpad_pkcs7(decrypt_AES_ECB(b64decode(h.read()), b"YELLOW SUBMARINE"))
	encrypt_AES_CTR(plaintext, key, get_random_bytes(16))
	
if __name__ == "__main__":
	main()
