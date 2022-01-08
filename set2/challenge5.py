from sys import path
path.append("../")

from Crypto import Random
from set2.challenge2 import encrypt_AES_ECB
from set1.challenge7 import decrypt_AES_ECB
from set2.challenge1 import pad_pkcs7

key = Random.get_random_bytes(16)

def parse_cookie(cookie):
	key_values = cookie.split("&")
	obj = {key_value.split('=')[0]:key_value.split('=')[1] for key_value in key_values}
	return obj

def profile_for(email):
	encoded_encrypted_email = encrypt_AES_ECB(b"email=" + email.replace(b'=', b'').replace(b'&', b'') + b"&uid=10&role=user", key)
	return encoded_encrypted_email

def decrypt_profile(profile):
	return decrypt_AES_ECB(profile, key)

def become_admin():
	block_size = 16 # I think we can assume this is the case, but if needed it can be easily deduced
	# we need to create a block that is equal to "admin" padded with pkcs7
	min_length = len("email=&uid=10&role=")
	wanted_length = ((min_length//block_size + 1) * block_size) - min_length
	email1 = b'A' * wanted_length
	cipher_text1 = profile_for(email1)
	body = cipher_text1[:-1 * block_size]
	
	injection = pad_pkcs7(b"admin", block_size)
	min_length_email = len("email=")
	email2 = b'A' * (block_size - min_length_email) + injection
	cipher_text2 = profile_for(email2)
	head = cipher_text2[block_size: block_size * 2]
	
	return body + head
	
def main():
	cookie = "foo=bar&baz=qux&zap=zazzle"
	admin = become_admin()
	print(decrypt_profile(admin))	
if __name__ == "__main__":
	main()
