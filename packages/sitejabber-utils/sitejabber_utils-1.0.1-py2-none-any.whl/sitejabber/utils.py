import base64
import hashlib
import hmac
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

def decrypt(string, key):
	"""
	Decrypt a string
	Args:
		param string: Base 64 encoded string
		param key: Encryption key
	Returns:
		Decrypted string
	"""
	string = base64.b64decode(string)

	iv = string[:AES.block_size]
	hash = string[AES.block_size:AES.block_size + 32]
	ciphertext = string[AES.block_size + 32:]
	key = hashlib.sha256(key.encode('utf8')).digest()

	if hmac.new(key, ciphertext, digestmod=hashlib.sha256).digest() == hash:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		return Padding.unpad(cipher.decrypt(ciphertext), AES.block_size)
	else:
		return None

def encrypt(string, key):
	"""
	Encrypt a string
	Args:
		param string: String to encrypt
		param key: Encryption key
	Returns:
		Base 64 encoded string
	"""
	string = Padding.pad(string.encode('utf8'), AES.block_size)
	key = hashlib.sha256(key.encode('utf8')).digest()
	cipher = AES.new(key, AES.MODE_CBC)

	ciphertext = cipher.encrypt(string)
	hash = hmac.new(key, ciphertext, digestmod=hashlib.sha256).digest()

	return base64.b64encode(cipher.iv + hash + ciphertext)
