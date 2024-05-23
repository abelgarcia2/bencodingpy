"""
    Copyright (C) 2024  @abelgarcia2

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from io import BytesIO
from typing import Callable

from .exceptions import BdecodingError

def _get_encoder(data: str|int|list|dict) -> Callable[[str|int|list|dict], [str|int|list|dict]]:
    """
    Get function to encode from data type
    :param data: item to be encoded
    :type data: str|int|list|dict
    :returns: function to encode next item
    :rtype: (str|int|list|dict) -> bytes
    :raises ValueError: if data not matches any accepted type
    """
    if isinstance(data, str) or isinstance(data, bytes):
        return _encode_str
    elif isinstance(data, int):
        return _encode_int
    elif isinstance(data, list):
        return _encode_list
    elif isinstance(data, dict):
        return _encode_dict
    else:
        raise ValueError("Unexpected data type")

def _encode_str(str_data: str|bytes) -> bytes:
    """
    Encode a string
    :param str_data: string to be encoded
    :type str_data: str|bytes
    :returns: bencoded string
    :rtype: bytes
    """
    if isinstance(str_data, str):
        str_data = bytes(str_data, encoding='utf-8')
    return bytes(f'{len(str_data)}:', encoding='utf-8') + str_data

def _encode_int(int_data: int) -> bytes:
    """
    Encode a int number
    :param int_data: int to be encoded
    :type int_data: int
    :returns: bencoded integer
    :rtype: bytes
    """
    return bytes(f'i{int_data}e', encoding='utf-8')

def _encode_list(list_data: list) -> bytes:
    """
    Encode a list
    :param list_data: list to be encoded
    :type list_data: list
    :returns: bencoded list
    :rtype: bytes
    """
    encoded_list = b'l'

    for item in list_data:
        encoder = _get_encoder(item)
        encoded_list += encoder(item)
    
    return encoded_list + b'e'

def _encode_dict(dict_data: dict) -> bytes:
    """
    Encode a dict
    :param dict_data: dict to be encoded
    :type dict_data: dict
    :returns: bencoded dict
    :rtype: bytes
    """
    encoded_dict = b'd'

    previous_key = list(dict_data.keys())[0]
    for key, value in dict_data.items():
        if not isinstance(key, str):
            raise TypeError('Dictionary keys must be strings')
        if key < previous_key:
            raise ValueError('Dict keys must appear in sorted order')
        previous_key = key

        key_encoder = _get_encoder(key)
        value_encoder = _get_encoder(value)

        encoded_dict += key_encoder(key)
        encoded_dict += value_encoder(value)
    
    return encoded_dict + b'e'

def encode(data: str|int|list|dict) -> bytes:
    """
    Encodes provided data
    :param data: data to be encoded
    :type data: str|int|list|dict
    :returns: bencoded data
    :rtype: bytes
    """
    encoder = _get_encoder(data)

    try:
        return encoder(data)
    except Exception as e:
        raise BdecodingError(e)