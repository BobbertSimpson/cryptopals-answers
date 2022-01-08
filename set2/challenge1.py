from Crypto.Random import random
from Crypto import Random

def pad_pkcs7(string, pad_length):
	missing = (pad_length - len(string)%pad_length)% pad_length
	return string + bytes(chr(missing), 'utf8') * missing

def unpad_pkcs7(string, pad_length):
	padding_size = string[-1]
	padding = padding_size * bytes([padding_size])
	if len(string) % pad_length == 0:
		return string
	if padding_size >= pad_length:
		return string
	if padding == string[len(string) - padding_size:]:
		return string[:len(string) - padding_size]
	print(string)
	raise Exception("Bad padding")
	

def main():
	print(unpad_pkcs7(b"ICE ICE BABY", 16))

if __name__ == "__main__":
	main()
