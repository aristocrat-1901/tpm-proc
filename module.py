from enum import Enum
from encrypt_methods import enc_dec_replace, enc_dec_shift


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Container:
    def __init__(self):
        self.start_node = None
        self.size = 0


def container_add(container, data):
    if container.start_node is None:
        container.start_node = Node(data)
    else:
        n = container.start_node
        while n.next:
            n = n.next
        n.next = Node(data)

    container.size += 1


def container_clear(container):
    container.start_node = None
    container.size = 0


def container_read_from(container, stream):
    while line := stream.readline():
        item = text_read_from(stream, line)
        container_add(container, item)


def container_write_to(container, stream):
    stream.write(f'Container has {container.size} elements\n\n')

    if container.start_node != None:
        n = container.start_node
        while n:
            text_write_to(n.data, stream)
            n = n.next
        stream.write('\n')


def text_read_from(stream, line):
    k = int(line)

    text = Text()
    text.line_symbol = stream.readline().rstrip('\n')
    if k == 1:
        text.key = Type.replacement
        text.obj = Replace()
        replace_read_from(text.obj, stream, text.line_symbol)
    elif k == 2:
        text.key = Type.shift
        text.obj = Shift()
        shift_read_from(text.obj, stream, text.line_symbol)
    else:
        return 0

    return text


def text_write_to(text, stream):
    if text.key == Type.replacement:
        stream.write('[Replacement method]\n')
        stream.write(f'String: {text.line_symbol}\n')
        replace_write_to(text.obj, stream)
    elif text.key == Type.shift:
        stream.write('[Shift method]\n')
        stream.write(f'String: {text.line_symbol}\n')
        shift_write_to(text.obj, stream)
    else:
        stream.write('Error type\n')


def replace_read_from(text, stream, line):
    print(line)
    text.encrypt_line = enc_dec_replace(line)



def replace_write_to(text, stream):
    stream.write(f'Encrypt message: {text.encrypt_line}\n')


def shift_read_from(text, stream, line):
    text.key = int(stream.readline())
    text.encrypt_line = enc_dec_shift(line, text.key)


def shift_write_to(text, stream):
    stream.write(f'Key = {text.key}\nEncrypt message : {text.encrypt_line}\n')


class Text:
    def __init__(self):
        self.line_symbol = None  # строка символов
        self.key = None  # номер способа шифрования
        self.obj = None  # способ шифрования


class Replace:
    def __init__(self):
        self.encrypt_line = None


class Shift:
    def __init__(self):
        self.key = None
        self.encrypt_line = None


class Type(Enum):
    replacement = 1
    shift = 2
