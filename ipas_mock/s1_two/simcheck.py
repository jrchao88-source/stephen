"""比對 s1_two 題目與舊題（官方歷屆 400、R1~R6、必考百題含兩個備份、set3、pred_v3）及兩回彼此的相似度。
用法：python3 simcheck.py R1.txt [R2.txt] [-v] [-top N]"""
import sys, os, re, glob, json, difflib, statistics
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
PUN = re.compile(r'[\s\W_]+', re.U)
def norm(s): return PUN.sub('', s)
def qtext(q): return norm(q['stem'] + ''.join(q['opts'][k] for k in 'ABCD'))
def corpus():
    out = []
    for q in json.load(open(os.path.join(R, 'ref/official_junior_questions.json'), encoding='utf-8')):
        out.append((f"官方{q['exam']}-{q['subject']}-{q['n']}", norm(q['text'])))
    files = (glob.glob(os.path.join(R, 'mock/R*-S*.txt')) + glob.glob(os.path.join(R, 'pred/P-S*.txt'))
             + glob.glob(os.path.join(R, 'pred/backup_v*/P-S*.txt')) + glob.glob(os.path.join(R, 'set3/S[12].txt'))
             + glob.glob(os.path.join(R, 'pred_v3/S[12].txt')))
    for f in sorted(files):
        tag = os.path.relpath(f, R)
        for q in parse(f): out.append((f"{tag}#{q['n']}", qtext(q)))
    return out
def best(t, C):
    b = (0, '')
    for name, c in C:
        sm = difflib.SequenceMatcher(None, t, c, autojunk=False)
        if sm.real_quick_ratio() <= b[0] or sm.quick_ratio() <= b[0]: continue
        r = sm.ratio()
        if r > b[0]: b = (r, name)
    return b
def check(path, C, others=(), thr=0.45, verbose=False):
    res = []
    for q in parse(path):
        t = qtext(q)
        b = best(t, C + [x for x in others if not x[0].startswith(os.path.basename(path) + '#' + str(q['n']) + '$')])
        res.append((q['n'], b[0], b[1]))
        if verbose or b[0] >= thr: print(f"  q{q['n']:>2} {b[0]:.3f} {b[1]}" + ('  <== 超過' if b[0] >= thr else ''))
    v = [r for _, r, _ in res]
    mx = max(res, key=lambda x: x[1])
    print(f"{os.path.basename(path)}: 中位數 {statistics.median(v):.3f} 最高 {mx[1]:.3f} (q{mx[0]} ↔ {mx[2]}) 超過{thr}: {sum(x>=thr for x in v)}")
    return res
if __name__ == '__main__':
    C = corpus(); print('舊題總數', len(C))
    paths = [a for a in sys.argv[1:] if a.endswith('.txt')]
    own = {p: [(f"{os.path.basename(p)}#{q['n']}$", qtext(q)) for q in parse(p)] for p in paths}
    allres = []
    for p in paths:
        others = [x for pp, xs in own.items() if pp != p for x in xs]
        r = check(p, C, others, verbose='-v' in sys.argv)
        allres += [(os.path.basename(p), n, s, m) for n, s, m in r]
    allres.sort(key=lambda x: -x[2])
    print('最高 8 題：')
    for f, n, s, m in allres[:8]: print(f'  {f} 第{n}題 {s:.3f} ↔ {m}')
