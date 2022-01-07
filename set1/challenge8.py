from Crypto.Cipher.AES import block_size
def number_of_repetitions_ECB(cipher_text):
	blocks = [cipher_text[i * block_size: i * block_size + block_size] for i in range(int(len(cipher_text) / block_size))]
	repetitions = len(blocks) - len(set(blocks))
	return repetitions
def detect_ecb_encryption(cipher_texts):
	max_score = -1
	max_index = -1
	index = 0
	for cipher_text in cipher_texts:
		repetitions = number_of_repetitions(cipher_text)
		if repetitions > max_score:
			max_score = repetitions
			max_index = index
		index += 1
	return (max_index, max_score)

def main():
	cipher_texts = [bytes.fromhex(line.strip()) for line in open("data/8.txt")]
	answer = detect_ecb_encryption(cipher_texts)
	print("The index is:" , answer[0], "\nAnd the number of repetitions is:", answer[1])
				
if __name__ == "__main__":
	main()
