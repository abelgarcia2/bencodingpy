from unittest import TestCase
from src.bencodingpy.exceptions import BdecodingEncodingError
from src.bencodingpy import encode

class TestString(TestCase):
    def test_word(self):
        self.assertEqual(encode('spam'), b'4:spam')
    
    def test_with_spaces(self):
        self.assertEqual(encode('s p a m'), b'7:s p a m')
    
    def test_one_char(self):
        self.assertEqual(encode('a'), b'1:a')

class TestInt(TestCase):
    def test_positive(self):
        self.assertEqual(encode(155), b'i155e')

    def test_negative(self):
        self.assertEqual(encode(-155), b'i-155e')

    def test_zero(self):
        self.assertEqual(encode(0), b'i0e')

    def test_minus_zero(self):
        self.assertEqual(encode(-0), b'i0e')

class TestList(TestCase):
    def test_strings(self):
        self.assertEqual(encode(['spam', 'eggs']), b'l4:spam4:eggse')

    def test_strings(self):
        self.assertEqual(encode([84, 65]), b'li84ei65ee')

    def test_dicts(self):
        self.assertEqual(encode([{'cow': 'moo'}, {'spam': 'eggs'}]), b'ld3:cow3:mooed4:spam4:eggsee')

class TestDict(TestCase):
    def test_string(self):
        self.assertEqual(encode({'cow': 'moo', 'spam': 'eggs'}), b'd3:cow3:moo4:spam4:eggse')

    def test_integer(self):
        self.assertEqual(encode({'cow': 999, 'spam': 999}), b'd3:cowi999e4:spami999ee')

    def test_list(self):
        self.assertEqual(encode({'cow': ['spam', 'eggs']}), b'd3:cowl4:spam4:eggsee')

    def test_dict(self):
        self.assertEqual(encode({'cow': {'spam': 'eggs'}}), b'd3:cowd4:spam4:eggsee')

    def test_sorted(self):
        with self.assertRaisesRegex(BdecodingEncodingError, 'Dict keys must appear in sorted order'):
            encode({'moo': 'spam', 'cow': 'eggs'})
            
    def test_no_string_keys(self):
        with self.assertRaisesRegex(BdecodingEncodingError, 'Dictionary keys must be strings'):
            encode({1: 'moo', 'spam': 'eggs'})