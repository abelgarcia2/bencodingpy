# Simple bencoding decode/encode library 🔖

## Install
```python
pip install bencodingpy
```

## Usage

### Decode
```python
>>> from bencodingpy import decode

>>> decode(b'4:spam')
'spam'

>>> decode(b'i1234e')
1234

>>> decode(b'l4:spam4:eggse')
['spam', 'eggs']

>>> decode(b'd4:spaml1:a1:bee ')
{'spam': ['a', 'b']}

>>> with open('debian-12.5.0-amd64-netinst.iso.torrent', 'rb') as file:
...     decoded_torrent = decode(file)
...     print(decoded_torrent['announce'])
... 
http://bttracker.debian.org:6969/announce
```

### Encode
```python
>>> from bencodingpy import encode

>>> encode('spam')
b'4:spam'

>>> encode(1234)
b'i1234e'

>>> encode(['spam', 'eggs'])
b'l4:spam4:eggse'

>>> encode({'spam': ['a', 'b']})
b'd4:spaml1:a1:bee'
```