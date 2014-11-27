import argparse
from collections import OrderedDict
from phylopylib.io import read_list_file, read_seq_file, write_file


# Option parser
parser = argparse.ArgumentParser(description='Rename sequences in a sequence file')
parser.add_argument('-n', '--names', default='names.txt',
                    help='provide a list file contains original names and target names')
parser.add_argument('-i', '--input', default='input.seq',
                    help='provide a input sequence file')
parser.add_argument('-f', '--file', choices=['seq', 'phy', 'nex', 'meg'], default='seq',
                    help='output file type')
parser.add_argument('-o', '--output', default='output',
                    help='output file name')


def main():
    args = parser.parse_args()
    names = [n.split() for n in read_list_file(args.names)]
    seqs = read_seq_file(args.input, missing=False)
    r_seqs = OrderedDict()

    i = 0
    for m, n in names:
        if m in seqs:
            r_seqs[n] = seqs[m]
        else:
            i += 1
            print('Missing individual: %s' % m)
    if i > 0:
        print('Totally missing individuals: %d' % i)

    f = '%s.renamed.%s' % (args.output, args.file)
    write_file(args.file, f, r_seqs)


if __name__ == '__main__':
    main()
