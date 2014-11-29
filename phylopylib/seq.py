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
