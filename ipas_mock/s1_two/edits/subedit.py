"""在指定題號、指定選項（或 S=題幹）中做字串替換。用法：python3 edits/subedit.py draft.txt edits/xxx.tsv（每行：題號<TAB>選項字母<TAB>舊<TAB>新）"""
import re, sys
d, e = sys.argv[1], sys.argv[2]
blocks = re.split(r'(?m)^(?=## )', open(d, encoding='utf-8').read())
idx = {int(re.match(r'## (\d+)', b).group(1)): i for i, b in enumerate(blocks) if b.startswith('## ')}
for line in open(e, encoding='utf-8'):
    if not line.strip() or line.startswith('#'): continue
    n, k, old, new = line.rstrip('\n').split('\t')
    b = blocks[idx[int(n)]]; lines = b.split('\n')
    hit = 0
    for j, l in enumerate(lines):
        if l.startswith(f'({k}) ') and old in l:
            lines[j] = l.replace(old, new, 1); hit += 1
    assert hit == 1, (n, k, old)
    blocks[idx[int(n)]] = '\n'.join(lines)
open(d, 'w', encoding='utf-8').write(''.join(blocks)); print('ok')
