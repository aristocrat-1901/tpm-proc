import io
import pytest
from module import ReplaceNum, replace_num_read_from, replace_num_write_to


@pytest.mark.parametrize("line,enc",
                         [('it is new method', '105116321051153211010111932109101116104111100'),
                          ('It is test method', '73116321051153211610111511632109101116104111100')])
def test_read_from(line, enc):
    obj = ReplaceNum()
    replace_num_read_from(obj, line)

    assert obj.encrypt_line == enc


@pytest.mark.parametrize("enc_line",
                         ['105116321051153211010111932109101116104111100',
                          '73116321051153211610111511632109101116104111100'])
def test_write_to(enc_line):
    obj = ReplaceNum()
    obj.encrypt_line = enc_line
    output = io.StringIO()
    replace_num_write_to(obj, output)
    output.seek(0)
    test_output = io.StringIO(f'Encrypt message: {enc_line}\n')

    assert output.read() == test_output.read()
