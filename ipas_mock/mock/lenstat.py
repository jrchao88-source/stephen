import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_mock import parse
def L(s): return len(s.replace(' ', ''))
def stat(path, verbose=False):
    qs = parse(path); longest = []
    for q in qs:
        lens = {k: L(v) for k, v in q['opts'].items()}
        a = lens[q['ans']]; mx = max(v for k, v in lens.items() if k != q['ans'])
        if a >= mx: longest.append(q['n'])
        if verbose: print(q['n'], q['ans'], lens, 'LONGEST' if a >= mx else '', f'margin={a-mx}')
    return qs, longest
if __name__ == '__main__':
    for p in sys.argv[1:]:
        qs, lg = stat(p, verbose='-v' in os.environ.get('V', ''))
        print(os.path.basename(p), '正解為最長(含並列):', len(lg), ' 非最長:', 50 - len(lg), ' 題號:', lg)
