from sys import path
path.append("../")

def unpad_pkcs7(string):
	if len(string) == 0:
		raise Exception("The length of the string has to be more than one")
	padding_size = string[-1]
	if padding_size * bytes([padding_size]) == string[len(string) - padding_size:]:
		return string[:len(string) - padding_size]
	raise Exception("Bad padding")

def main():
	print(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04"))
	print(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x03"))

if __name__ == "__main__":
	main()
