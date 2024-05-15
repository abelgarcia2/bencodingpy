from io import BytesIO, SEEK_CUR

INT_TYPE = b'i'
LIST_TYPE = b'l'
DICT_TYPE = b'd'

END_CHAR = b'e'

SEPARATOR = b':'

def _get_decoder(char: str):
    if char.isdigit():
        return decode_str
    elif char == INT_TYPE:
        return decode_int
    elif char == LIST_TYPE:
        return decode_list
    elif char == DICT_TYPE:
        return decode_dict
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

def decode_str(data: BytesIO) -> str:
    data.seek(-1, SEEK_CUR)
    str_length = int(_read_to(SEPARATOR, data))

    readed_str = data.read(str_length)

    try:
        result_str = str(readed_str.decode())
    except UnicodeDecodeError:
        result_str = readed_str

    return result_str

def decode_int(data: BytesIO) -> int:
    result_number = b''
    while True:
        char = data.read(1)

        if char == END_CHAR:
            break

        result_number += char
    
    return int(result_number)

def decode_list(data: BytesIO) -> list:
    result_list = []

    while True:
        char = data.read(1)

        if char == END_CHAR:
            break

        decoder = _get_decoder(char)

        result_list.append(decoder(data))
    
    return result_list

def decode_dict(data: BytesIO):
    result_dict = {}

    key = None
    i = 0
    while True:
        readed_char = data.read(1)

        if readed_char == END_CHAR:
            break

        decoder = _get_decoder(readed_char)

        if i%2 == 0:
            key = decoder(data)
        else:
            result_dict[key] = decoder(data)
        
        i += 1
    
    return result_dict

def decode(data: BytesIO):
    first_char = data.read(1)
    decoder = _get_decoder(first_char)
    return decoder(data)