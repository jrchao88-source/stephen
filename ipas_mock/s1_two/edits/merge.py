"""把 edits/<file> 中的題目區塊（依題號）替換進 draft。用法：python3 edits/merge.py draft_R1.txt edits/r1_replace.txt"""
import re, sys
def blocks(t):
    return {int(re.match(r'## (\d+)', b).group(1)): b.rstrip('\n') + '\n\n' for b in re.split(r'(?m)^(?=## )', t) if b.startswith('## ')}
d, r = sys.argv[1], sys.argv[2]
B = blocks(open(d, encoding='utf-8').read()); N = blocks(open(r, encoding='utf-8').read())
B.update(N)
open(d, 'w', encoding='utf-8').write(''.join(B[k] for k in sorted(B)).rstrip('\n') + '\n')
print('replaced', sorted(N))
