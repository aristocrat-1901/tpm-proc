import sys
from module import (Container, container_read_from,
                    container_write_to,
                    container_clear,
                    container_sort,
                    container_write_to_replace)


def main():
    if len(sys.argv) != 3:
        print('\nФайлы ввода/вывода не выбраны!')
        infile = 'in.txt'
        outfile = 'out.txt'
        print(f'Будут использованы стандартные {infile} и {outfile}!\n')
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]

    input_file = open(infile, "r")
    print('Start')
    cont = Container()
    container_read_from(cont, input_file)
    input_file.close()

    print('Filled container')
    container_sort(cont)  # сортировка контейнера по количеству символов в строке
    output_file = open(outfile, "w")
    container_write_to(cont, output_file)
    # container_write_to_replace(cont, output_file) # запись в файл только одного метода Replace

    container_clear(cont)
    print('Empty container')
    container_write_to(cont, output_file)
    output_file.close()


if __name__ == '__main__':
    main()
