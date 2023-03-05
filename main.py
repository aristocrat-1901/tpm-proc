import sys
from module import (Container, container_read_from,
                    container_write_to,
                    container_clear,
                    container_sort)


def main():
    if len(sys.argv) != 3:
        print('\nФайлы ввода/вывода не выбраны! Будут использованы стандартные in.txt и out.txt\n')
        infile = 'in.txt'
        outfile = 'out.txt'
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    input_file = open(infile, "r")

    print('Start')

    cont = Container()
    container_read_from(cont, input_file)

    print('Filled container')
    container_sort(cont)
    output_file = open(outfile, "w")
    container_write_to(cont, output_file)

    container_clear(cont)

    print('Empty container')
    container_write_to(cont, output_file)

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
