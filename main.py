import sys
from module import (Container, container_read_from,
                    container_write_to,
                    container_clear)


def main():
    input_file = open(sys.argv[1], "r")

    print('Start')

    cont = Container()
    container_read_from(cont, input_file)

    print('Filled container')

    output_file = open(sys.argv[2], "w")
    container_write_to(cont, output_file)

    container_clear(cont)

    print('Empty container')
    container_write_to(cont, output_file)

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    main()
