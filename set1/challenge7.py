from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_AES_ECB(key, cipher_text):
	cypher = AES.new(key, AES.MODE_ECB)
	plain_text = cypher.decrypt(cipher_text).decode('utf8')
	return plain_text
def main():
	header = open("data/7.txt", 'r')
	cipher_text = b64decode(header.read())
	header.close()
	plain_text = decrypt_AES_ECB(b"YELLOW SUBMARINE", cipher_text)
	print(plain_text)

if __name__ == "__main__":
	main()
