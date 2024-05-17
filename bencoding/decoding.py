from io import BytesIO, SEEK_CUR

INT_PREFIX = b'i'
LIST_PREFIX = b'l'
DICT_PREFIX = b'd'

END_CHAR = b'e'

SEPARATOR_CHAR = b':'

def _get_decoder(char: bytes):
    if char.isdigit():
        return _decode_str
    elif char == INT_PREFIX:
        return _decode_int
    elif char == LIST_PREFIX:
        return _decode_list
    elif char == DICT_PREFIX:
        return _decode_dict
    elif char == END_CHAR:
        pass

def _read_to(char: str, data: BytesIO) -> bytes:
    buf = b''
    while True:
        readed_char = data.read(1)

        if readed_char == char:
            break

        buf += readed_char

    return buf

def _decode_str(data: BytesIO) -> str:
    data.seek(-1, SEEK_CUR)
    str_length = int(_read_to(SEPARATOR_CHAR, data))

    readed_str = data.read(str_length)

    try:
        result_str = str(readed_str.decode())
    except UnicodeDecodeError:
        result_str = readed_str

    return result_str

def _decode_int(data: BytesIO) -> int:
    result_number = b''
    while True:
        char = data.read(1)

        if char == END_CHAR:
            break

        result_number += char
    
    return int(result_number)

def _decode_list(data: BytesIO) -> list:
    result_list = []

    while True:
        char = data.read(1)

        if char == END_CHAR:
            break

        decoder = _get_decoder(char)

        result_list.append(decoder(data))
    
    return result_list

def _decode_dict(data: BytesIO) -> dict:
    result_dict = {}

    key = None
    while True:
        readed_char = data.read(1)

        if readed_char == END_CHAR:
            break

        decoder = _get_decoder(readed_char)

        if key:
            result_dict[key] = decoder(data)
            key = None
        else:
            key =  decoder(data)
    
    return result_dict

def decode(data: BytesIO):
    first_char = data.read(1)
    decoder = _get_decoder(first_char)
    return decoder(data)