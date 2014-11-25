import argparse
from collections import OrderedDict
from phylopylib.io import read_list_file, read_seq_file, write_file


# Option parser
parser = argparse.ArgumentParser(description='Combine multiple genes sequences to NEXUS/PHYLIP/MEGA format')
parser.add_argument('-g', '--genes', default='genes.txt',
                    help='provide a list file contains all genes need to be combined')
parser.add_argument('-n', '--names', default='names.txt',
                    help='provide a list file contains all individual names')
parser.add_argument('-f', '--file', choices=['seq', 'phy', 'nex', 'meg'], default='seq',
                    help='output file type')
parser.add_argument('-o', '--output', default='combine',
                    help='output file name')
parser.add_argument('-p', '--partition', action='store_true',
                    help='output a RAxML-style partition file for combined sequences')
parser.add_argument('-s', '--separate', action='store_true',
                    help='output separated formatted gene file contained missing individuals')


def main():

    # parse command-line options
    args = parser.parse_args()
    genes = read_list_file(args.genes)
    names = read_list_file(args.names)
    
    # read sequences and record genes lengths
    seqs = OrderedDict()
    seq_lengths = OrderedDict()
    for g in genes:
        seq_file = '%s.seq' % g
        seqs[g] = read_seq_file(seq_file)
        seq_lengths[g] = len(list(seqs[g].values())[0])

    # generate nexus file for each gene
    n_seqs = OrderedDict()
    for g in genes:
        missing = []
        unused = []
        n_seqs[g] = OrderedDict()
        for n in names:
            if n in seqs[g]:
                n_seqs[g][n] = seqs[g][n]
            else:
                missing.append(n)
                n_seqs[g][n] = '?' * seq_lengths[g]
        if len(missing) > 0:
            print('Gene %s missed: %s' % (g, ', '.join(missing)))
        for n in seqs[g]:
            if n not in names:
                unused.append(n)
        if len(unused) > 0:
            print('Gene %s unused: %s' % (g, ', '.join(unused)))
        if args.separate:
            f = '%s.comb.%s' % (g, args.file)
            write_file(args.file, f, n_seqs[g])

    # combine
    c_seqs = OrderedDict()
    for n in names:
        c_seqs[n] = ''.join([n_seqs[g][n] for g in genes])
    f = '%s.%s' % (args.output, args.file)
    write_file(args.file, f, c_seqs)

    # partition file
    if args.partition:
        x, y = 0, 0
        partition = ''
        for g in genes:
            x, y = y+1, y+seq_lengths[g]
            partition += 'DNA, %s = %d-%d\n' % (g, x, y)
        open('partition.txt', 'w').write(partition)

if __name__ == '__main__':
    main()