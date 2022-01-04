import base64
from challenge3 import solve_one_letter_xor, get_score

def hamming(string1, string2):
	counter = 0
	for i in range(len(string1)):
		c1 = string1[i]
		c2 = string2[i]
		for i in range(8):
			counter += ((c1 >> i) & 1) ^ (1 & (c2 >> i))
	return counter

def min_numbers(array, n):
	answer = []
	for i in range(n):
		m = min(array)
		array.remove(m)
		answer.append(m)
	return answer
		
def main():
	header = open("data/6.txt", 'r')
	text = base64.b64decode(("".join(header.read().split())))
	scores = []
	for KEYSIZE in range(2, 41):
		part1 = text[0:KEYSIZE];
		part2 = text[KEYSIZE:KEYSIZE * 2]
		part3 = text[KEYSIZE * 2:KEYSIZE * 3]
		part4 = text[KEYSIZE * 3:KEYSIZE * 4]
		score = (hamming(part1, part2) + hamming(part2, part3) + hamming(part3, part4))/(KEYSIZE * 3);
		scores.append([score, KEYSIZE])

	results = min_numbers(scores, 3)
	print("The found keys are: ")
	all_answers = []
	for _, KEYSIZE in results:
		parts = []
		for i in range(KEYSIZE):
			parts.append(text[i::KEYSIZE])
		answer_parts = []
		for part in parts:
			stuff = solve_one_letter_xor(part)
			print(chr(stuff[0]), end="")
			answer_parts.append(bytes(stuff[2], 'utf8'))
		print()
		answer = b''
		size = len(answer_parts[-1])
		for i in range(size):
			for j in range(KEYSIZE):
				answer += bytes(chr(answer_parts[j][i]), 'utf8')
		for i in range(KEYSIZE):
			if len(answer_parts[i]) > size:
				answer += bytes(chr(answer_parts[i][-1]), 'utf8')
			else:
				break;
		all_answers.append(answer)
	print()
	max = 0;
	index = 0
	max_index = -1
	for answer in all_answers:
		score = get_score(answer.decode('utf8'))
		if score > max:
			final_answer = answer
			max = score
			max_index = index
		index += 1
	print(all_answers[max_index].decode('utf8')) 
	# print(final_answer.decode('utf8'))
if __name__ == "__main__":
	main()
