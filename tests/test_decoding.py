from unittest import TestCase
from bencoding import BdecodingError
from bencoding.decoding import decode

class TestString(TestCase):
    def test_word(self):
        self.assertEqual(decode('4:spam'), 'spam')

    def test_with_spaces(self):
        self.assertEqual(decode('7:s p a m'), 's p a m')

    def test_one_char(self):
        self.assertEqual(decode('1:a'), 'a')

class TestInteger(TestCase):
    def test_positive(self):
        self.assertEqual(decode('i123456e'), 123456)
        self.assertEqual(decode('i34e'), 34)

    def test_negative(self):
        self.assertEqual(decode('i-34e'), -34)

    def test_zero(self):
        self.assertEqual(decode('i0e'), 0)

    def test_minus_zero(self):
        with self.assertRaisesRegex(BdecodingError, 'Integer -0 is invalid'):
            decode('i-0e')
    
    def test_leading_zero(self):
        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('i-034e')
        
        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('i034e')

class TestList(TestCase):
    def test_string(self):
        self.assertEqual(decode('l4:spam4:eggse'), ['spam', 'eggs'])

    def test_integer(self):
        self.assertEqual(decode('li84ei65ee'), [84, 65])
        with self.assertRaisesRegex(BdecodingError, 'Leading zero number is invalid'):
            decode('li-34ei056ee')
        
    def test_dict(self):
        self.assertEqual(decode('ld3:cow3:mooed4:spam4:eggsee'), [{'cow': 'moo'}, {'spam': 'eggs'}])

class TestDict(TestCase):
    def test_string(self):
        self.assertEqual(decode('d3:cow3:moo4:spam4:eggse'), {'cow': 'moo', 'spam': 'eggs'})

    def test_integer(self):
        self.assertEqual(decode('d3:cowi999e4:spami999ee'), {'cow': 999, 'spam': 999})
    
    def test_list(self):
        self.assertEqual(decode('d3:cowl4:spam4:eggsee'), {'cow': ['spam', 'eggs']})
    
    def test_dict(self):
        self.assertEqual(decode('d3:cowd4:spam4:eggsee'), {'cow': {'spam': 'eggs'}})
    
    def test_ordered(self):
        with self.assertRaisesRegex(BdecodingError, 'Dict keys must appear in sorted order'):
            decode('d3:moo4:spam3:cow4:eggse')
    
    def test_string_keys(self):
        with self.assertRaisesRegex(BdecodingError, 'Dictionary keys must be strings'):
            decode('di1e3:moo4:spam4:eggse')