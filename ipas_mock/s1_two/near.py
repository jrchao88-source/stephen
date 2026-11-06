"""列出每題在舊題中「概念最接近」的前 N 題（字元雙字組 cosine，比對題幹＋正解），供人工檢查切入角度是否重複。
用法：python3 near.py draft_R1.txt [起題 迄題] [N]"""
import sys, os, re, json, glob, math
from collections import Counter
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
PUN = re.compile(r'[\s\W_A-Za-z0-9]+', re.U)
def bg(s):
    s = PUN.sub('', s); return Counter(s[i:i+2] for i in range(len(s)-1))
def cos(a, b):
    n = sum(a[k]*b[k] for k in a if k in b)
    return n / (math.sqrt(sum(v*v for v in a.values())) * math.sqrt(sum(v*v for v in b.values())) + 1e-9)
items = []
for q in json.load(open(os.path.join(R, 'ref/official_junior_questions.json'), encoding='utf-8')):
    t = q['text']; items.append((f"官方{q['exam']}-{q['subject']}-{q['n']}", t))
files = (glob.glob(os.path.join(R, 'mock/R*-S1.txt')) + glob.glob(os.path.join(R, 'pred/P-S1.txt'))
         + glob.glob(os.path.join(R, 'pred/backup_v*/P-S1.txt')) + glob.glob(os.path.join(R, 'set3/S1.txt')) + glob.glob(os.path.join(R, 'pred_v3/S1.txt'))
         + [a for a in sys.argv[1:] if a.endswith('.txt') and a != sys.argv[1]])
for f in sorted(files):
    for q in parse(f): items.append((os.path.relpath(f, R) + '#' + str(q['n']), q['stem'] + ' ▶' + q['opts'][q['ans']]))
V = [(n, t, bg(t)) for n, t in items]
args = [a for a in sys.argv[2:] if not a.endswith('.txt')]
lo, hi = (int(args[0]), int(args[1])) if len(args) >= 2 else (1, 50)
N = int(args[2]) if len(args) >= 3 else 3
for q in parse(sys.argv[1]):
    if not lo <= q['n'] <= hi: continue
    v = bg(q['stem'] + q['opts'][q['ans']])
    top = sorted(((cos(v, b), n, t) for n, t, b in V), reverse=True)[:N]
    print(f"## {q['n']} {q['stem'][:60]}")
    for s, n, t in top: print(f"   {s:.2f} {n} {t.replace(chr(10),'')[:110]}")
