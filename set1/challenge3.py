from string import ascii_uppercase, ascii_lowercase

letter_frequency = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}
def xor_bytes(string, key):
	result = b""
	for i in range(len(string)):
		result += bytes(chr(string[i] ^ key[i % len(key)]), 'utf8');
	return result
def get_score(string):
	score = 0
	for letter in string:
		score += letter_frequency.get(letter, 0)
	return score
def solve_one_letter_xor(string):
	max_frequency = [-1, 0, ''] #the index and the value of the byte with the highest frequency and the string
	for xor in range(256):	
		all_frequency = []
		answer = xor_bytes(string, bytes(chr(xor), 'utf8')).decode('utf8').lower()
		frequency = get_score(answer);
		
		if max_frequency[0] == -1 or max_frequency[1] < frequency:
			max_frequency[0] = xor
			max_frequency[1] = frequency
			max_frequency[2] = answer
	return max_frequency;

def main():
	string = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
	# string = bytes("ETAOIN SHRDLU", 'ascii');
	max_frequency = solve_one_letter_xor(string)
	print(bytes(max_frequency[2].upper(), 'ascii'), "was obtained by the key \"" + chr(max_frequency[0]) + "\" with the Score: ", str(round(max_frequency[1], 1)));

if __name__ == "__main__":
	main()		
