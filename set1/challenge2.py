string = bytes.fromhex("1c0111001f010100061a024b53535009181c");
xor = bytes.fromhex("686974207468652062756c6c277320657965")
answer = bytes()

for i in range(len(string)):
	answer += bytes(chr(string[i] ^ xor[i % len(xor)]), 'utf8')

print(answer.hex())
