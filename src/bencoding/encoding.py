from io import BytesIO

def _get_encoder(data):
    if isinstance(data, str) or isinstance(data, bytes):
        return _encode_str
    elif isinstance(data, int):
        return _encode_int
    elif isinstance(data, list):
        return _encode_list
    elif isinstance(data, dict):
        return _encode_dict

def _encode_str(str_data: str|bytes) -> str:
    a = bytes(f'{len(str_data)}:', encoding='utf-8')
    b = (bytes(str_data, encoding='utf-8') if isinstance(str_data, str) else str_data)

    c = a + b
    return bytes(f'{len(str_data)}:', encoding='utf-8') + (bytes(str_data, encoding='utf-8') if isinstance(str_data, str) else str_data)

def _encode_int(int_data: int) -> str:
    return bytes(f'i{int_data}e', encoding='utf-8')

def _encode_list(list_data: list) -> str:
    encoded_list = b'l'

    for item in list_data:
        encoder = _get_encoder(item)
        encoded_list += encoder(item)
    
    return encoded_list + b'e'

def _encode_dict(dict_data: dict):
    encoded_dict = b'd'

    for key, value in dict_data.items():
        key_encoder = _get_encoder(key)
        value_encoder = _get_encoder(value)

        encoded_dict += key_encoder(key)
        encoded_dict += value_encoder(value)
    
    return encoded_dict + b'e'

def encode(data):
    encoder = _get_encoder(data)

    return encoder(data)