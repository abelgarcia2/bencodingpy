from unittest import TestCase

from bencoding import BdecodingError
from bencoding import BdecodingError
from bencoding.decoding import decode
from bencoding.encoding import encode

class TestDecoding(TestCase):
    def test_string(self):
        self.assertEqual(decode('4:spam'), 'spam')
        self.assertEqual(decode('7:s p a m'), 's p a m')
        self.assertEqual(decode('1:a'), 'a')

    def test_integer(self):
        self.assertEqual(decode('i123456e'), 123456)
        self.assertEqual(decode('i0e'), 0)
        self.assertEqual(decode('i34e'), 34)
        self.assertEqual(decode('i-34e'), -34)

        with self.assertRaisesRegex(BdecodingError, 'Integer -0 is invalid'):
            decode('i-0e')
        
        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('i-034e')
        
        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('i034e')
        
    def test_list(self):
        self.assertEqual(decode('l4:spam4:eggse'), ['spam', 'eggs'])
        self.assertEqual(decode('li84ei65ee'), [84, 65])

        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('li-34ei056ee')
        
        self.assertEqual(decode('ld3:cow3:mooed4:spam4:eggsee'), [{'cow': 'moo'}, {'spam': 'eggs'}])
    
    def test_dict(self):
        self.assertEqual(decode('d3:cow3:moo4:spam4:eggse'), {'cow': 'moo', 'spam': 'eggs'})
        self.assertEqual(decode('d3:cowi999e4:spami999ee'), {'cow': 999, 'spam': 999})
        self.assertEqual(decode('d3:cowl4:spam4:eggsee'), {'cow': ['spam', 'eggs']})
        self.assertEqual(decode('d3:cowd4:spam4:eggsee'), {'cow': {'spam': 'eggs'}})

        with self.assertRaisesRegex(BdecodingError, 'Dict keys must appear in sorted order'):
            decode('d3:moo4:spam3:cow4:eggse')
        
        with self.assertRaisesRegex(BdecodingError, 'Dictionary keys must be strings'):
            decode('di1e3:moo4:spam4:eggse')

class EncodingTest (TestCase):
    def test_string(self):
        self.assertEqual(encode('spam'), b'4:spam')
        self.assertEqual(encode('s p a m'), b'7:s p a m')
        self.assertEqual(encode('a'), b'1:a')
    
    def test_int(self):
        self.assertEqual(encode(155), b'i155e')
        self.assertEqual(encode(-155), b'i-155e')
        self.assertEqual(encode(0), b'i0e')
        self.assertEqual(encode(-0), b'i0e')
    
    def test_list(self):
        self.assertEqual(encode(['spam', 'eggs']), b'l4:spam4:eggse')

        self.assertEqual(encode([84, 65]), b'li84ei65ee')

        self.assertEqual(encode([{'cow': 'moo'}, {'spam': 'eggs'}]), b'ld3:cow3:mooed4:spam4:eggsee')
    
    def test_dict(self):
        self.assertEqual(encode({'cow': 'moo', 'spam': 'eggs'}), b'd3:cow3:moo4:spam4:eggse')
        self.assertEqual(encode({'cow': 999, 'spam': 999}), b'd3:cowi999e4:spami999ee')
        self.assertEqual(encode({'cow': ['spam', 'eggs']}), b'd3:cowl4:spam4:eggsee')
        self.assertEqual(encode({'cow': {'spam': 'eggs'}}), b'd3:cowd4:spam4:eggsee')
    
        with self.assertRaisesRegex(BdecodingError, 'Dict keys must appear in sorted order'):
            encode({'moo': 'spam', 'cow': 'eggs'})
            
        with self.assertRaisesRegex(BdecodingError, 'Dictionary keys must be strings'):
            encode({1: 'moo', 'spam': 'eggs'})


class TorrentFile(TestCase):
    def test(self):
        with open('tests/torrent/debian-12.5.0-amd64-netinst.iso.torrent', 'rb') as file:
            decoded_torrent = decode(file)
            self.assertEqual(len(decoded_torrent), 6)
            self.assertEqual(len(decoded_torrent['info']['pieces']), 50320)

            reencoded_torrent = encode(decoded_torrent)
            redecoded_torrent = decode(reencoded_torrent)

            self.assertEqual(len(redecoded_torrent['info']['pieces']), 50320)
            self.assertEqual(redecoded_torrent, decoded_torrent)
            self.assertEqual(redecoded_torrent['info']['pieces'], decoded_torrent['info']['pieces'])