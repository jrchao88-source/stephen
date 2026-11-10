import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mock'))
from parse_mock import parse
ABS = ['一定', '完全', '任何', '所有', '一律', '永遠', '保證', '絕對', '百分之百']
for f in sys.argv[1:]:
    for q in parse(f):
        for k, v in q['opts'].items():
            a = [w for w in ABS if w in v]; b = [w for w in ('因為', '所以') if w in v]
            if a or b: print(f"{f[-6:-4]} q{q['n']:>2} {k}{'*' if k==q['ans'] else ' '} abs={','.join(a):8} cz={','.join(b):6} {v}")
