from challenge3 import xor_bytes

def main():
	string = bytes("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", 'utf8')
	key = bytes("ICE", 'utf8');
	answer = xor_bytes(string, key).hex()
	print(answer[:75] + "\n" + answer[75:])

if __name__ == "__main__":
	main()
