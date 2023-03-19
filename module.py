from enum import Enum
from encrypt_methods import enc_dec_replace, enc_dec_shift, enc_dec_replace_num
import sys


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
        item = text_read_from(line)
        if item is not None:
            container_add(container, item)


def container_write_to(container, stream):
    stream.write(f'Container has {container.size} elements\n\n')

    if container.start_node is not None:
        n = container.start_node
        while n:
            text_write_to(n.data, stream)
            n = n.next
        stream.write('\n')


def container_sort(container):
    if container.start_node is None:
        print('Empty list')
    else:
        n1 = container.start_node
        n2 = container.start_node.next
        while n1 is not None:
            while n2 is not None:
                if number_of_symbols(n1.data) < number_of_symbols(n2.data):  # > сортировка по убыванию длины строк
                    n1.data, n2.data = n2.data, n1.data
                n2 = n2.next
            n1 = n1.next
            n2 = container.start_node


def container_check_texts(container):
    texts_1 = []
    n = container.start_node
    while n is not None:
        texts_1.append(n.data)
        n = n.next

    texts_2 = texts_1.copy()

    for text_1 in texts_1:
        for text_2 in texts_2:
            check_texts(text_1.obj, text_2.obj)


def check_texts(text_1, text_2):
    match text_1, text_2:
        case Replace(), Replace():
            print("Шифрование одного типа: Replace and Replace")

        case Replace(), Shift():
            print("Шифрование разного типа: Replace and Shift")

        case Replace(), ReplaceNum():
            print("Шифрование разного типа: Replace and ReplaceNum")

        case Shift(), Replace():
            print("Шифрование разного типа: Shift and Replace")

        case Shift(), Shift():
            print("Шифрование одного типа: Shift and Shift")

        case Shift(), ReplaceNum():
            print("Шифрование разного типа: Shift and ReplaceNum")

        case ReplaceNum(), Replace():
            print("Шифрование разного типа: ReplaceNum and Replace")

        case ReplaceNum(), Shift():
            print("Шифрование разного типа: ReplaceNum and Shift")

        case ReplaceNum(), ReplaceNum():
            print("Шифрование одного типа: ReplaceNum and ReplaceNum")

        case _:
            print('Неизвестный тип')
            return

    print(f"Первый: {text_1}, второй: {text_2}")
    print()


def container_write_to_replace(container, stream):
    print("Only replacement method")

    n = container.start_node
    while n is not None:
        if n.data.key == Type.replacement:
            text_write_to(n.data, stream)
        n = n.next
    stream.write('\n')


def text_read_from(line):
    list_param = line.rstrip('\n').split('; ')
    if len(list_param) < 3:
        print('Неверный формат входной строки!')
        return
    try:
        k = int(list_param[0])
    except ValueError:
        print('Первый параметр некорректен!')
        return
    text = Text()
    text.line_symbol = list_param[1]
    text.author = list_param[2]
    if k == 1:
        text.key = Type.replacement
        text.obj = Replace()
        replace_read_from(text.obj, text.line_symbol)
    elif k == 2:
        text.key = Type.shift
        text.obj = Shift()
        try:
            key = int(list_param[3])
        except LookupError:
            print("Для 2 метода не задан ключ!")
            return
        except ValueError:
            print("Ключ для 2 метода должен быть числом!")
            return
        shift_read_from(text.obj, key, text.line_symbol)
    elif k == 3:
        text.key = Type.replacement_by_num
        text.obj = ReplaceNum()
        replace_num_read_from(text.obj, text.line_symbol)
    else:
        print(f"Недопустимый тип метода {k}!")
        return

    return text


def text_write_to(text, stream):
    if text.key == Type.replacement:
        try:
            stream.write('[Replacement method]\n')
            stream.write(f'String: {text.line_symbol}\n')
            stream.write(f'Author: {text.author}\n')
            stream.write(f'String length: {number_of_symbols(text)}\n')
            replace_write_to(text.obj, stream)
        except OSError:
            print('Ошибка записи в файл!')
            sys.exit(1)
    elif text.key == Type.shift:
        try:
            stream.write('[Shift method]\n')
            stream.write(f'String: {text.line_symbol}\n')
            stream.write(f'Author: {text.author}\n')
            stream.write(f'String length: {number_of_symbols(text)}\n')
            shift_write_to(text.obj, stream)
        except OSError:
            print('Ошибка записи в файл!')
            sys.exit(1)
    elif text.key == Type.replacement_by_num:
        try:
            stream.write('[Replacement by numbers method]\n')
            stream.write(f'String: {text.line_symbol}\n')
            stream.write(f'Author: {text.author}\n')
            stream.write(f'String length: {number_of_symbols(text)}\n')
            replace_write_to(text.obj, stream)
        except OSError:
            print('Ошибка записи в файл!')
            sys.exit(1)
    else:
        stream.write('Ошибка при записи! Некорректный тип метода!\n')


def replace_read_from(text, line):
    text.encrypt_line = enc_dec_replace(line)


def replace_write_to(text, stream):
    stream.write(f'Encrypt message: {text.encrypt_line}\n')


def shift_read_from(text, key, line):
    text.key = key
    text.encrypt_line = enc_dec_shift(line, text.key)


def shift_write_to(text, stream):
    stream.write(f'Key = {text.key}\nEncrypt message : {text.encrypt_line}\n')


def number_of_symbols(text):
    return len(text.line_symbol)


def replace_num_read_from(text, line):
    text.encrypt_line = enc_dec_replace_num(line)


def replace_num_write_to(text, stream):
    stream.write(f'Encrypt message: {text.encrypt_line}\n')


class Text:
    def __init__(self):
        self.line_symbol = None  # строка символов
        self.key = None  # номер способа шифрования
        self.obj = None  # способ шифрования
        self.author = None  # владелец строки


class Replace:
    def __init__(self):
        self.encrypt_line = None


class Shift:
    def __init__(self):
        self.key = None
        self.encrypt_line = None


class ReplaceNum:
    def __init__(self):
        self.encrypt_line = None


class Type(Enum):
    replacement = 1
    shift = 2
    replacement_by_num = 3
