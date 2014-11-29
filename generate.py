import argparse
from phylopylib.io import read_seq_file, write_file
from phylopylib.seq import split_codons, delete_gaps


# Option parser
parser = argparse.ArgumentParser(description='Generate specific format file')
parser.add_argument('input',
                    help='provide a input sequence file (exclude ".seq")')
parser.add_argument('-d', '--delete-gaps', action='store_true',
                    help='delete gaps')
parser.add_argument('-f', '--offset', type=int, default=0,
                    help='offset of reading framework, for splitting codons')
parser.add_argument('-m', '--missing', action='store_true',
                    help='convert leading or ending gaps to missing')
parser.add_argument('-o', '--output', default='',
                    help='output file name')
parser.add_argument('-s', '--split-codons', action='store_true',
                    help='split sequences to three codons')
parser.add_argument('-t', '--type', choices=['seq', 'phy', 'nex', 'meg', 'fas'], default='seq',
                    help='output file type')


def main():
    args = parser.parse_args()
    if args.output == '':
        args.output = args.input
    seqs = read_seq_file(args.input+'.seq', missing=args.missing)

    if args.split_codons:
        r_seqs = split_codons(seqs, offset=args.offset)
        if args.delete_gaps:
            r_seqs = map(delete_gaps, r_seqs)
        for i in (1, 2, 3):
            f = '%s_codon%d.%s' % (args.output, i, args.type)
            write_file(args.type, f, r_seqs[i-1])
    else:
        if args.delete_gaps:
            seqs = delete_gaps(seqs)
        f = '%s.%s' % (args.output, args.type)
        write_file(args.type, f, seqs)


if __name__ == '__main__':
    main()