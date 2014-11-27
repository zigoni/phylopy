import argparse
from collections import OrderedDict
from phylopylib.io import read_seq_file, write_file


# Option parser
parser = argparse.ArgumentParser(description='Generate specific format file')
parser.add_argument('-i', '--input', default='input.seq',
                    help='provide a input sequence file')
parser.add_argument('-f', '--file', choices=['phy', 'nex', 'meg', 'fas'], default='fas',
                    help='output file type')
parser.add_argument('-o', '--output', default='output',
                    help='output file name')


def main():
    args = parser.parse_args()
    seqs = read_seq_file(args.input, missing=False)
    f = '%s.%s' % (args.output, args.file)
    write_file(args.file, f, seqs)


if __name__ == '__main__':
    main()