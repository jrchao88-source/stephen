"""比對 pred_v3 題目與舊題（官方歷屆、R1~R6、必考百題含備份、set3）的相似度。
用法：python3 simcheck.py S1.txt [S2.txt] [-v 門檻]"""
import sys, os, re, glob, json, difflib, statistics
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
PUN = re.compile(r'[\s\W_]+', re.U)
def norm(s): return PUN.sub('', s)
def corpus():
    out = []
    for q in json.load(open(os.path.join(R, 'ref/official_junior_questions.json'), encoding='utf-8')):
        out.append((f"官方{q['exam']}-{q['subject']}-{q['n']}", norm(q['text'])))
    files = glob.glob(os.path.join(R, 'mock/R*-S*.txt')) + glob.glob(os.path.join(R, 'pred/P-S*.txt')) + glob.glob(os.path.join(R, 'pred/backup_v*/P-S*.txt')) + glob.glob(os.path.join(R, 'set3/S[12].txt'))
    for f in sorted(files):
        tag = os.path.relpath(f, R)
        for q in parse(f):
            out.append((f"{tag}#{q['n']}", norm(q['stem'] + ''.join(q['opts'][k] for k in 'ABCD'))))
    return out
def check(path, C, thr=0.55, verbose=False):
    res = []
    for q in parse(path):
        t = norm(q['stem'] + ''.join(q['opts'][k] for k in 'ABCD'))
        best = (0, '')
        for name, c in C:
            sm = difflib.SequenceMatcher(None, t, c, autojunk=False)
            if sm.real_quick_ratio() <= best[0] or sm.quick_ratio() <= best[0]: continue
            r = sm.ratio()
            if r > best[0]: best = (r, name)
        res.append((q['n'], best[0], best[1]))
        if verbose or best[0] >= thr: print(f"  q{q['n']:>2} {best[0]:.3f} {best[1]}" + ('  <== 超過' if best[0] >= thr else ''))
    v = [r for _, r, _ in res]
    print(f"{os.path.basename(path)}: 中位數 {statistics.median(v):.3f} 最高 {max(v):.3f} (q{max(res,key=lambda x:x[1])[0]}) 超過{thr}: {sum(x>=thr for x in v)}")
    return res
if __name__ == '__main__':
    C = corpus(); print('舊題總數', len(C))
    for p in [a for a in sys.argv[1:] if a.endswith('.txt')]: check(p, C, verbose='-v' in sys.argv)
