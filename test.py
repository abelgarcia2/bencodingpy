from bencoding.decoding import decode
from bencoding.encoding import encode

from  io import BytesIO

with open('archlinux-2024.05.01-x86_64.iso.torrent', 'rb') as file:
    decoded_data = decode(file)