from sys import path
path.append("../")


def unpad_pkcs7(string, pad_length):
	padding_size = string[-1]
	padding = padding_size * bytes([padding_size])
	if len(string) % pad_length == 0 and padding_size > pad_length:
		return string
	if padding_size >= pad_length:
		return string
	if padding == string[len(string) - padding_size:]:
		return string[:len(string) - padding_size]
	print(string)
	raise Exception("Bad padding")

def main():
	print(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04", 	16))
	print(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x03", 16))

if __name__ == "__main__":
	main()
