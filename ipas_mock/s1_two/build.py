"""s1_two：draft_Rx.txt（正解一律寫在 A）→ Rx.txt（科目一兩回）：
1. 依 SEQ 重排選項，讓正解落在指定字母（同步替換題幹與解說中的 (A)~(D) 參照）。
2. 把考點行的 @sub:<子考點名稱> / @cat:<大類代碼> 換成參考檔中實際存在的題號。"""
import re, sys, os, json, random
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
SEQ = {'R1': 'DCAACCAADBBACACAADDCCBBDACBDDCBAABBDBBCBBDCDCAACDD',
       'R2': 'CACCDDCAADAACBDDBCCBAABBDDBDCBCDCBACCBAABDBCADABAD'}
SUBS = {x['name']: x for x in json.load(open(os.path.join(R, 'ref/subtopics.json'), encoding='utf-8'))}
TOP = json.load(open(os.path.join(R, 'ref/topic_stats.json'), encoding='utf-8'))['topics']
EX = {'114-四': '114-4', '115-一': '115-1', '115-二': '115-2', '115-三': '115-3'}
LAB = {}
for l in open(os.path.join(R, 'ref/labels.txt'), encoding='utf-8'):
    k, *v = l.split()
    if v: LAB[k] = v
def cite_sub(name):
    x = SUBS[name]; parts = []
    for ex, ns in x['qs'].items():
        if ns: parts.append(EX[ex] + ' ' + '、'.join(f'第{n}題' for n in ns[:2]))
    return '歷屆同考點：' + '；'.join(parts)
def cite_cat(code, salt):
    subj = '一' if code[0] == 'T' else '二'
    parts = []
    rnd = random.Random(code + str(salt))
    for ex in EX:
        ns = [i + 1 for i, c in enumerate(LAB[f'{ex}-{subj}']) if c == code]
        if ns: parts.append(EX[ex] + ' ' + '、'.join(f'第{n}題' for n in sorted(rnd.sample(ns, min(2, len(ns))))))
    short = re.sub(r'（.*', '', TOP[code]['name'])
    return f'歷屆同大類（{short}）：' + '；'.join(parts)
def build(key):
    txt = open(os.path.join(D, f'draft_{key}.txt'), encoding='utf-8').read()
    blocks = re.split(r'(?m)^(?=## )', txt); out = []; i = 0
    for b in blocks:
        if not b.startswith('## '): out.append(b); continue
        m = re.match(r'## (\d+) \| ([^|]+) \| A\n', b); assert m, b[:40]
        tgt = SEQ[key][i]; i += 1
        lines = b.rstrip('\n').split('\n')
        opt = {}; idx = {}
        for j, l in enumerate(lines):
            mo = re.match(r'^\(([A-D])\) (.*)$', l)
            if mo: opt[mo.group(1)] = mo.group(2); idx[mo.group(1)] = j
        others = [k for k in 'BCD']
        newpos = [k for k in 'ABCD' if k != tgt]   # 錯誤選項保持原本相對順序
        mp = {'A': tgt}; mp.update(dict(zip(others, newpos)))
        neo = {mp[k]: v for k, v in opt.items()}
        for k in 'ABCD': lines[idx[k]] = f'({k}) {neo[k]}'
        lines[0] = f'## {m.group(1)} | {m.group(2)} | {tgt}'
        def remap(s): return re.sub(r'\(([A-D])\)', lambda mm: f'({mp[mm.group(1)]})', s)
        for j, l in enumerate(lines):
            if j in idx.values() or j == 0: continue
            if l.startswith('考點：'):
                l = re.sub(r'@sub:(.+)$', lambda mm: cite_sub(mm.group(1)), l)
                l = re.sub(r'@cat:(\w+)$', lambda mm: cite_cat(mm.group(1), m.group(1)), l)
                lines[j] = l
            else: lines[j] = remap(l)
        out.append('\n'.join(lines) + '\n\n')
    open(os.path.join(D, f'{key}.txt'), 'w', encoding='utf-8').write(''.join(out).rstrip('\n') + '\n')
if __name__ == '__main__':
    for k in sys.argv[1:]: build(k)
