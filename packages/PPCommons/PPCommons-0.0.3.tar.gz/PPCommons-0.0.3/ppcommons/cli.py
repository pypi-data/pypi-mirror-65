import argparse


def main():
    parser = argparse.ArgumentParser(description="PPCommons Argument Parser")
    parser.add_argument('-hello', type=str, nargs=1, metavar='name', help='Says Hello')
    args = parser.parse_args()
    print('hello {} from ppcommons'.format(args.name[0]))


if __name__ == '__main__':
    main()
