from challenge3 import solve_one_letter_xor


def main():
	file_handle = open("data/4.txt", "r")
	file = file_handle.read().split();
	max = [-1, 0, ''];
	counter = 0;
	for line in file:
		current = solve_one_letter_xor(bytes.fromhex(line));
		current.append(counter);
		counter += 1
		if current[1] > max[1]:
			max = current
	print(str(max[2][:-1]) , "is the found text, and was found using the character \"" + chr(max[0]) + "\" on line", max[3])
if __name__ == "__main__":
	main()
