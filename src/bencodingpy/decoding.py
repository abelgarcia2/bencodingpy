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

from io import BufferedReader, BytesIO, SEEK_CUR
import re
from typing import Callable

from .exceptions import BdecodingEncodingError

INT_PREFIX = b'i'
LIST_PREFIX = b'l'
DICT_PREFIX = b'd'

END_CHAR = b'e'
STRING_SEPARATOR_CHAR = b':'

LEADING_ZERO_REGEX = re.compile(r'^-?0+\d+')


def _get_decoder(
    char: bytes
) -> Callable[[BufferedReader], str | int | list | dict]:
    """
    Guesses next item type from preceding character
    :param char: a single byte character
    :type char: bytes
    :returns: function to decode next characters
    :rtype: (BufferedReader) -> str|int|list|dict
    :raises ValueError: if char not is a valid char
    """
    if char.isdigit():
        return _decode_str
    elif char == INT_PREFIX:
        return _decode_int
    elif char == LIST_PREFIX:
        return _decode_list
    elif char == DICT_PREFIX:
        return _decode_dict
    else:
        raise ValueError("Unexpected char when guessing type")


def _read_to(char: str, data: BufferedReader) -> bytes:
    """
    Read from buffer until char is found
    :param char: char to stop
    :type char: str
    :param data: buffer to read
    :type data: BufferedReader
    :returns: readed bytes
    :rtype: bytes
    """
    buff = b''
    while (readed_char := data.read(1)) != char:
        buff += readed_char

    return buff


def _convert_to_buffered_reader(data: str | bytes) -> BufferedReader:
    """
    Convert data to BufferedReader
    :param data: Data to be decoding
    :type data: str|bytes
    :returns: BufferedReader containing data
    :rtype: BufferedReader
    """
    if isinstance(data, str):
        data = bytes(data, encoding='utf-8')
    return BufferedReader(BytesIO(data))


def _decode_str(data: BufferedReader) -> str | bytes:
    """
    Reads an string or bytes from buffer
    :param data: buffer to read
    :type data: BufferedReader
    :returns: readed string or buffer
    :rtype: str|bytes
    """
    data.seek(-1, SEEK_CUR)
    str_length = int(_read_to(STRING_SEPARATOR_CHAR, data))

    readed_str = data.read(str_length)

    try:
        result_str = str(readed_str.decode())
    except UnicodeDecodeError:
        result_str = readed_str

    return result_str


def _decode_int(data: BufferedReader) -> int:
    """
    Reads an int from buffer
    :param data: buffer to read
    :type data: BufferedReader
    :returns: readed int
    :rtype: int
    :raises ValueError: if int has leading zeros or int is -0
    """
    result_number = _read_to(END_CHAR, data)
    result_number = result_number.decode()
    if result_number == '-0':
        raise ValueError("Integer -0 is invalid")

    if re.match(LEADING_ZERO_REGEX, result_number):
        raise ValueError("Leading zero number is invalid")

    return int(result_number)


def _decode_list(data: BufferedReader) -> list:
    """
    Reads a list from buffer
    :param data: buffer to read
    :type data: BufferedReader
    :returns: readed list
    :rtype: list
    """
    result_list = []

    while (char := data.read(1)) != END_CHAR:
        decoder = _get_decoder(char)
        result_list.append(decoder(data))

    return result_list


def _decode_dict(data: BufferedReader) -> dict:
    """
    Reads a dict from buffer
    :param data: buffer to read
    :type data: BufferedReader
    :returns: readed list
    :rtype: dict
    :raises TypeError: if a dict key is not a string
    :raises ValueError: if dict keys not ordered
    """
    result_dict = {}

    key = None
    old_key = ""
    while (readed_char := data.read(1)) != END_CHAR:
        decoder = _get_decoder(readed_char)
        if key is not None:
            result_dict[key] = decoder(data)
            old_key = key
            key = None
        else:
            key = decoder(data)

            if not isinstance(key, str):
                raise TypeError("Dictionary keys must be strings")
            if not key > old_key:
                raise ValueError("Dict keys must appear in sorted order")

    return result_dict


def decode(data: BufferedReader | bytes | str) -> str | int | list | dict:
    """
    Decode bencoding data
    :param data: buffer, bytes or string to decode
    :type data: BufferedReader|bytes|str
    :returns: decoded data
    :rtype: str|int|list|dict
    :raises BdecodingError: if an error occurs during decoding
    """
    try:
        if not isinstance(data, BufferedReader):
            data = _convert_to_buffered_reader(data)
        first_char = data.read(1)
        decoder = _get_decoder(first_char)
        return decoder(data)
    except Exception as e:
        raise BdecodingEncodingError(e)
