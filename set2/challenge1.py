
def pad_pkcs7(string, pad_length):
	missing = (pad_length - len(string)%pad_length)% pad_length
	return string + bytes(chr(missing), 'utf8') * missing

def unpad_pkcs7(string, pad_length):
	padding_size = string[-1]
	padding = padding_size * bytes(chr(padding_size), 'utf8')
	if padding_size >= pad_length or padding_size > len(string):
		return string
	elif padding != string[len(string) - padding_size:]:
		return string
	else:
		return string[:len(string) - padding_size]

def main():
	string = bytes("YELLOW SUBMARINE", 'utf8')
	pad_length = int(input())
	padded_string = pad_pkcs7(string, pad_length)
	print(padded_string)
	print(unpad_pkcs7(padded_string, pad_length))
	
if __name__ == "__main__":
	main()
