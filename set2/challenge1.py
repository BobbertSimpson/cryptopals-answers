from Crypto.Random import random
from Crypto import Random

def pad_pkcs7(string, pad_length=16):
	missing = pad_length - len(string)%pad_length
	if missing == 0:
		missing = pad_length
	return string + bytes(chr(missing), 'utf8') * missing

def unpad_pkcs7(string):
	if len(string) == 0:
		raise Exception("The length of the string has to be more than one")
	padding_size = string[-1]
	if padding_size * bytes([padding_size]) == string[len(string) - padding_size:]:
		return string[:len(string) - padding_size]
	#print(len(string)/16)
	raise Exception("Bad padding")
	

def main():
	print(unpad_pkcs7(pad_pkcs7(b"ICE ICE BABY")))

if __name__ == "__main__":
	main()
