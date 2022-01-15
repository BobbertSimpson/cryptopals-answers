from sys import path
path.append("../")

from set2.challenge1 import unpad_pkcs7
from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_AES_ECB(cipher_text, key):
	cipher = AES.new(key, AES.MODE_ECB)
	plain_text = cipher.decrypt(cipher_text)
	return plain_text
def main():
	header = open("data/7.txt", 'r')
	cipher_text = b64decode(header.read())
	header.close()
	plain_text = decrypt_AES_ECB(cipher_text, b"YELLOW SUBMARINE")
	print(plain_text.decode('utf8'))

if __name__ == "__main__":
	main()
