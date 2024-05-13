""" Callate docstring """

def decide():
    char = f.read(1)
    if not char.isdigit():
        return char
    
    number = char.decode('utf-8')
    while True:
        char = f.read(1)
        if char == b':':
            break
        number += char.decode('utf-8')
    
    return number
        
def read_dict():
    data = {}

    key = ''
    i = 0
    while True:
        char = decide()
        if char == b'e':
            break
        if i%2 == 0:
            key = read_data(char)
        else:
            data[key] = read_data(char)
        i += 1
    return data


def read_str(str_length: int) -> str:
    string = f.read(str_length)
    return string.decode('utf-8') if string.isascii() else string

def read_int() -> int:
    number = ''
    while True:
        char = f.read(1)
        if char == b'e':
            break
        number += char.decode('utf-8')
    
    return int(number)

def read_list() -> list:
    data = []

    while True:
        char = decide()
        if char == b'e':
            break
        data.append(read_data(char))
    
    return data

def read_data(char:bytes):
    if char.isdigit():
        str_length = int(char)
        return read_str(str_length)
    elif char == b'i':
        return read_int()
    elif char == b'l':
        return read_list()
    elif char == b'd':
        return read_dict()
    elif char == b'e':
        pass
        

with open('debian-12.5.0-amd64-netinst.iso.torrent', 'rb') as f:
    result = read_data(f.read(1))

    print(result)