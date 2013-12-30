import unittest
from test import test_support

from coins.address import *

class BitcoinAddressTest(unittest.TestCase):

	def setUp(self):
		self.reference = {
			'passphrase': 'correct horse battery staple',
			'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
			'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
			'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
			'wif_private_key':'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
			'address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
		}
		self.address = BitcoinAddress.from_secret_exponent(self.reference['hex_private_key'])

	def tearDown(self):
		pass

	def test_hex_private_key(self):
		self.assertTrue(self.address.hex_private_key() == self.reference['hex_private_key'])

	def test_wif_private_key(self):
		self.assertTrue(self.address.wif_private_key() == self.reference['wif_private_key'])

	def test_address(self):
		self.assertTrue(str(self.address) == self.reference['address'])

	def test_hex_hash160(self):
		self.assertTrue(self.address.hex_hash160() == self.reference['hex_hash160'])

	def test_public_key(self):
		self.assertTrue(self.address.hex_public_key() == self.reference['hex_public_key'])

class AltcoinAddressTest(unittest.TestCase):
	def setUp(self):
		self.reference = {
			'passphrase': 'correct horse battery staple',
			'hex_private_key': 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a',
			'hex_public_key': '0478d430274f8c5ec1321338151e9f27f4c676a008bdf8638d07c0b6be9ab35c71a1518063243acd4dfe96b66e3f2ec8013c8e072cd09b3834a19f81f659cc3455',
			'hex_hash160': 'c4c5d791fcb4654a1ef5e03fe0ad3d9c598f9827',
			'bitcoin_wif_pk':'5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS',
			'bitcoin_address': '1JwSSubhmg6iPtRjtyqhUYYH7bZg3Lfy1T',
			'litecoin_wif_pk': '6vcfLvDpYnHdbVxoQa6Lmo3k9iR5xVjKwwf3dp4XgmQT3QJywYi',
			'litecoin_address': 'LdAPi7uXrLLmeh7u57pzkZc3KovxEDYRJq',
			'namecoin_wif_pk': '74Pe3r1wxUzY8nHd2taLb5SqpAsxZK6q6VwUcQp7fPS11tYZd9P',
			'namecoin_address': 'NEWoeZ6gh4CGvRgFAoAGh4hBqpxizGT6gZ',
			'peercoin_wif_pk': '7ADsaYN3Wm2DYF2jkdSLT3FAZWj7WRdTTR9oLrsoeMTAVgq1Mho',
			'peercoin_address': 'PSXcbszYpbauNj6WF4AE9SWYjLjZArBajH',
			'primecoin_wif_pk': '6623w812F9NyDzSAk5aMvn4PFs28htfSGxtMY4s7qPEkhoV8sQS',
			'primecoin_address': 'AZiK6QTL6pksCrdjTdW2dRoNbCVNQ7zRs6',
		}
		self.bitcoin_address = BitcoinAddress.from_secret_exponent(self.reference['hex_private_key'])
		self.litecoin_address = LitecoinAddress.from_secret_exponent(self.reference['hex_private_key'])
		self.namecoin_address = NamecoinAddress.from_secret_exponent(self.reference['hex_private_key'])
		self.peercoin_address = PeercoinAddress.from_secret_exponent(self.reference['hex_private_key'])
		self.primecoin_address = PrimecoinAddress.from_secret_exponent(self.reference['hex_private_key'])

	def tearDown(self):
		pass

	def test_wif_private_key(self):
		self.assertTrue(self.bitcoin_address.private_key() == self.reference['bitcoin_wif_pk'])
		self.assertTrue(self.litecoin_address.private_key() == self.reference['litecoin_wif_pk'])
		self.assertTrue(self.namecoin_address.private_key() == self.reference['namecoin_wif_pk'])
		self.assertTrue(self.peercoin_address.private_key() == self.reference['peercoin_wif_pk'])
		self.assertTrue(self.primecoin_address.private_key() == self.reference['primecoin_wif_pk'])

	def test_address(self):
		self.assertTrue(str(self.bitcoin_address) == self.reference['bitcoin_address'])
		self.assertTrue(str(self.litecoin_address) == self.reference['litecoin_address'])
		self.assertTrue(str(self.namecoin_address) == self.reference['namecoin_address'])
		self.assertTrue(str(self.peercoin_address) == self.reference['peercoin_address'])
		self.assertTrue(str(self.primecoin_address) == self.reference['primecoin_address'])

class BitcoinBrainWalletAddressTest(BitcoinAddressTest):
	def setUp(self):
		BitcoinAddressTest.setUp(self)
		self.address = BitcoinAddress.from_passphrase(self.reference['passphrase'], num_words=4)

	def test_passphrase(self):
		self.assertTrue(self.address.passphrase() == self.reference['passphrase'])

class BitcoinAddressFromWIFTest(BitcoinAddressTest):
	def setUp(self):
		BitcoinAddressTest.setUp(self)
		self.address = BitcoinAddress.from_wif_private_key(self.reference['wif_private_key'])

from coins.utils import b58check_encode, b58check_decode, b58check_unpack, \
	is_wif_private_key, is_hex_private_key

class BitcoinUtilsTest(unittest.TestCase):
	def setUp(self):
		self.hex_private_key = 'c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a'
		self.wif_private_key = '5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS'
		self.version_byte = 128

	def tearDown(self):
		pass

	def test_b58check_encode_then_decode(self):
		bin_private_key = self.hex_private_key.decode('hex')
		wif_private_key = b58check_encode(bin_private_key, version_byte=self.version_byte)
		self.assertTrue(self.wif_private_key == wif_private_key)
		bin_private_key_verification = b58check_decode(wif_private_key)
		self.assertTrue(bin_private_key_verification == bin_private_key)

	def test_b58check_unpack_then_encode(self):
		version_byte, bin_private_key, checksum = b58check_unpack(self.wif_private_key)
		self.assertTrue(ord(version_byte) == self.version_byte)
		wif_private_key = b58check_encode(bin_private_key, version_byte=ord(version_byte))
		self.assertTrue(self.wif_private_key == wif_private_key)

	def test_is_wif_private_key(self):
		self.assertTrue(is_wif_private_key(self.wif_private_key))

	def test_is_hex_private_key(self):
		self.assertTrue(is_hex_private_key(self.hex_private_key))

def test_main():
	test_support.run_unittest(
		BitcoinAddressTest,
		AltcoinAddressTest,
		BitcoinBrainWalletAddressTest,
		BitcoinAddressFromWIFTest,
		BitcoinUtilsTest
	)

if __name__ == '__main__':
    test_main()