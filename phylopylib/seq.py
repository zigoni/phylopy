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


def delete_gap(seqs):
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