from sitejabber import utils
from unittest import TestCase

class TestUtils(TestCase):

	def test_encrypt_decrypt(self):
		string = "test string"
		key = "XlVzl5iwuIakc8FMlf2Ws2XCkMs6WVHh"

		self.assertEqual(string.encode('utf8'), utils.decrypt(utils.encrypt(string, key), key))

if __name__ == '__main__':
	unittest.main()
