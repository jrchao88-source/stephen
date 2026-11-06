"""檢查絕對用語與「因為／所以」在正解與錯誤選項中的分布（以 draft 為準：A 為正解）。"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mock'))
from parse_mock import parse
ABS = ['一定', '完全', '任何', '所有', '一律', '永遠', '保證', '絕對', '百分之百']
for f in sys.argv[1:]:
    qs = parse(f); ca = wa = cb = wb = 0; rows = []
    for q in qs:
        for k, v in q['opts'].items():
            a = any(w in v for w in ABS); b = ('因為' in v or '所以' in v)
            if k == q['ans']: ca += a; cb += b
            else: wa += a; wb += b
            if b and k != q['ans']: rows.append((q['n'], k))
    print(f, f'絕對用語 正解 {ca}/50={ca/50:.0%} 錯誤 {wa}/150={wa/150:.0%} | 因為/所以 正解 {cb}/50={cb/50:.0%} 錯誤 {wb}/150={wb/150:.0%}')
    if '-v' in os.environ.get('V', ''): print('  錯誤選項含因為/所以:', rows)
