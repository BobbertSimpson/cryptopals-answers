from sys import path
path.append("../")

from base64 import b64decode
from set3.challenge3 import crack_CTR_auto

# Too lazy  to write it
def main():
	h = open('data/20.txt', 'r')
	ciphertexts = h.read().split()
	ciphertexts = [b64decode(text) for text in ciphertexts]
	crack_CTR_auto(ciphertexts)
if __name__ == "__main__":
	main()
