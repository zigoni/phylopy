from collections import Counter
from collections import OrderedDict


# Convert gaps (-) in the beginning and the end to missing (?)
def gap2missing(seq):
    length = len(seq)

    def check(s):
        if s.startswith('-'):
            for i in range(0, length):
                if s[i]!='-':
                    return '?'*i+s[i:]
        else:
            return s
    seq = check(seq[::-1])
    seq = check(seq[::-1])
    return seq


# Delete gaps
def delete_gaps(seqs):
    seq_length = len(list(seqs.values())[0])
    seq_num = len(seqs)
    r_seqs = OrderedDict(zip(seqs.keys(), ['']*seq_num))
    for i in range(seq_length):
        status = Counter(seqs[n][i] for n in seqs)
        if status['-'] > 0:
            continue
        else:
            for n in seqs:
                r_seqs[n] += seqs[n][i]
    return r_seqs


# RY-encode
def ry_encode(seq):
    seq = seq.replace('G', 'A')
    seq = seq.replace('T', 'C')
    return seq


# Split codons
def split_codons(seqs, offset=0):
    r_seqs = [OrderedDict(), OrderedDict(), OrderedDict()]
    seq_length = len(list(seqs.values())[0])
    for i in range(seq_length):
        m = (i + 3 - offset) % 3
        for n in seqs:
            if n in r_seqs[m]:
                r_seqs[m][n] += seqs[n][i]
            else:
                r_seqs[m][n] = seqs[n][i]
    return r_seqs