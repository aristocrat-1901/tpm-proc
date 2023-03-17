import io
from module import Text, Replace, Shift, Type, text_read_from, text_write_to, number_of_symbols
import pytest


@pytest.mark.parametrize("test_input,line,author",
                         [("1; abc; I\n", 'abc', 'I'), ("2; hello; Roma; 3\n", 'hello', 'Roma')])
def test_read_from(test_input, line, author):
    text = text_read_from(test_input)

    assert text.line_symbol == line
    assert text.author == author


@pytest.mark.parametrize("line,author",
                         [('abcde', 'Boris'), ('test2', 'Arkasha')])
def test_write_to(line, author):
    output = io.StringIO()
    text = Text()
    text.line_symbol = line
    text.author = author
    text.key = Type.replacement
    text.obj = Replace()
    length = number_of_symbols(text)

    text_write_to(text, output)
    output.seek(0)

    test_str = f'[Replacement method]\n' \
               f'String: {line}\n' \
               f'Author: {author}\n' \
               f'String length: {length}\n' \
               f'Encrypt message: {text.obj.encrypt_line}\n'

    assert output.read() == test_str


@pytest.mark.parametrize("line,author,meth",
                         [('abcde', 'Boris', Type.replacement), ('test2', 'Arkasha', Type.shift)])
def test_write_to_replace(line, author, meth):
    output = io.StringIO()
    text = Text()
    text.line_symbol = line
    text.author = author
    if meth == Type.replacement:
        text.key = meth
        text.obj = Replace()
    else:
        text.key = 0
        text.obj = Shift()

    length = number_of_symbols(text)
    text_write_to(text, output)
    test_str = 'Ошибка при записи! Некорректный тип метода!\n'
    output.seek(0)
    if meth == Type.replacement:
        test_str = f'[Replacement method]\n' \
                   f'String: {line}\n' \
                   f'Author: {author}\n' \
                   f'String length: {length}\n' \
                   f'Encrypt message: {text.obj.encrypt_line}\n'

    assert output.read() == test_str


@pytest.mark.parametrize('mes, count', [
    ('hello world', 11),
    ('it is secret', 12),
    ('abcds', 5),
])
def test_number_sym(mes, count):
    text = Text()
    text.line_symbol = mes
    assert number_of_symbols(text) == count
