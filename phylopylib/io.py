import re
import sys
from collections import OrderedDict
from seq import gap2missing


# Read list file
def read_list_file(list_file):
    try:
        f = open(list_file).readlines()
    except IOError:
        sys.exit('File %s not exists!' % list_file)
    result = [line.strip() for line in f]
    return result


# Read sequence file
def read_seq_file(seq_file, missing=True, excluding_list=()):
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
            if missing:
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
        content += '%s%s\n' % (name.ljust(20), seqs[name])
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
        content += '%s%s\n' % (name.ljust(10), seqs[name])
    return content


# Generate mega file
def gen_meg_file(seqs):
    content = '#Mega\ntitle Seqs\n\n'
    for name in seqs:
        content += '#%s\n%s\n' % (name, seqs[name])
    return content


# Generate seq file
def gen_seq_file(seqs):
    content = ''
    for name in seqs:
        content += '%s%s\n' % (name.ljust(10), seqs[name])
    return content


# Generate fasta file
def gen_fas_file(seqs):
    content = ''
    for name in seqs:
        content += '>%s\n%s\n' % (name, seqs[name])
    return content


# Write formatted sequences file
def write_file(file_type, file_name, seqs):
    func_name = 'gen_%s_file' % file_type
    content = eval(func_name)(seqs)
    open(file_name, 'w').write(content)