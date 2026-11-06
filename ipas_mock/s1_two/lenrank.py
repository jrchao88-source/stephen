"""正解長度排名統計＋逐題列出各選項長度（draft 或成品皆可）。用法：python3 lenrank.py file [-v]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mock'))
from parse_mock import parse
def L(s): return len(s.replace(' ', ''))
for f in [a for a in sys.argv[1:] if a.endswith('.txt')]:
    ranks = [0]*4; rows = []
    for q in parse(f):
        lens = {k: L(v) for k, v in q['opts'].items()}; a = lens[q['ans']]
        r = sum(1 for k, v in lens.items() if k != q['ans'] and v > a)
        ranks[r] += 1; rows.append((q['n'], r, a, sorted((v for k, v in lens.items() if k != q['ans']), reverse=True)))
    print(f, '正解長度排名[最長,第2,第3,最短]:', ranks)
    if '-v' in sys.argv:
        for n, r, a, o in rows: print(f'  q{n:>2} rank{r+1} ans={a} others={o}')
