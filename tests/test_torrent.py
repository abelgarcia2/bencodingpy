from unittest import TestCase
from bencoding.encoding import encode
from bencoding.decoding import decode

class TestDecoding(TestCase):
    def setUp(self):
        self.torrent = open('tests/torrents/debian-12.5.0-amd64-netinst.iso.torrent', 'rb')
        self.decoded_torrent = decode(self.torrent)
    
    def test_length(self):
        self.assertEqual(len(self.decoded_torrent), 6)
    
    def test_pieces(self):
        self.assertEqual(len(self.decoded_torrent['info']['pieces']), 50320)
    
    def tearDown(self):
        self.torrent.close()

class TestCompare(TestCase):
    def setUp(self):
        self.torrent = open('tests/torrents/debian-12.5.0-amd64-netinst.iso.torrent', 'rb')
        self.decoded_torrent = decode(self.torrent)
        
        self.rencoded_torrent = encode(self.decoded_torrent)
        self.redecoded_torrent = decode(self.rencoded_torrent)
    
    def test_compare_length(self):
        self.assertEqual(len(self.decoded_torrent), 6)
        self.assertEqual(len(self.decoded_torrent['info']['pieces']), 50320)

        self.assertEqual(len(self.redecoded_torrent), 6)
        self.assertEqual(len(self.redecoded_torrent['info']['pieces']), 50320)
    
    def test_compare_torrent(self):
        self.assertEqual(self.redecoded_torrent, self.decoded_torrent)
        self.assertEqual(self.redecoded_torrent['info']['pieces'], self.decoded_torrent['info']['pieces'])
    
    def tearDown(self):
        self.torrent.close()