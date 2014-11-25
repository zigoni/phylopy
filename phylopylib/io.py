import re
import sys
from collections import OrderedDict


# Read list file
def read_list_file(list_file):
    try:
        f = open(list_file).readlines()
    except IOError:
        sys.exit('File %s not exists!' % list_file)
    result = [line.strip() for line in f]
    return result


# Read sequence file
def read_seq_file(seq_file, excluding_list=()):
    seqs = []
    pattern = r'^([\w\.-]+)\s+([\?ATGCRYKSMWBVDHN-]+)$'
    reg = re.compile(pattern)

    try:
        fl = open(seq_file).readlines()
    except IOError:
        print('Input file %s not exists!' % seq_file)
        sys.exit()

    j = 0
    for i in fl:
        j += 1
        s = reg.search(i)
        if s is not None:
            x = s.group(1)
            y = s.group(2)
            if x in excluding_list:
                continue
            y = gap2missing(y)
            seqs.append((x, y))
        else:
            raise Exception('Unexpected content in file %s line %d' % (seq_file, j))
    return OrderedDict(seqs)


# Generate nexus file
def gen_nex_file(seqs):
    n = len(seqs)
    l = len(list(seqs.values())[0])
    content = '''#NEXUS
BEGIN DATA;
dimensions ntax=%d nchar=%d;
format missing=?
[symbols="ABCDEFGHIKLMNPQRSTUVWXYZ"]
interleave datatype=DNA gap= -;

matrix
''' % (n, l)
    for name in seqs:
        seq = seqs[name]
        formatted_name = name.ljust(20)
        content += '%s%s\n' % (formatted_name, seq)
    content += ''';
END;
'''
    return content


# Generate phylip file
def gen_phy_file(seqs):
    n = len(seqs)
    l = len(list(seqs.values())[0])
    content = '%d %d\n' % (n, l)
    for name in seqs:
        seq = seqs[name]
        formatted_name = name.ljust(10)
        content += '%s%s\n' % (formatted_name, seq)
    return content

