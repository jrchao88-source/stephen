import re, sys, os, glob, json
from collections import Counter
D = os.path.dirname(os.path.abspath(__file__))
SEQ = dict(l.split() for l in open(os.path.join(D, 'answer_seq.txt')) if l.strip())
def parse(path):
    txt = open(path, encoding='utf-8').read()
    blocks = re.split(r'^## ', txt, flags=re.M)[1:]
    qs = []
    for b in blocks:
        lines = b.strip('\n').split('\n')
        m = re.match(r'^(\d+)\s*\|\s*([^|]+?)\s*\|\s*([A-D])\s*$', lines[0])
        if not m: raise ValueError(f'{path}: bad header: {lines[0]}')
        n, tags, ans = int(m.group(1)), [t.strip() for t in m.group(2).split(',')], m.group(3)
        body = lines[1:]
        opts, stem, exp, cur, topic = {}, [], '', None, ''
        for l in body:
            mo = re.match(r'^\(([A-D])\)\s*(.*)$', l)
            if mo: opts[mo.group(1)] = mo.group(2); cur = mo.group(1); continue
            if l.startswith('考點：'): topic = l[3:]; continue
            if l.startswith('解說：'): exp = l[3:]; cur = 'E'; continue
            if not l.strip(): continue
            if cur is None: stem.append(l)
            elif cur == 'E': exp += l
            else: opts[cur] += l
        qs.append(dict(n=n, tags=tags, ans=ans, stem='\n'.join(stem), opts=opts, exp=exp, topic=topic))
    return qs
def validate(path):
    key = os.path.basename(path)[:-4]
    qs = parse(path); errs = []
    if [q['n'] for q in qs] != list(range(1, 51)): errs.append(f'numbering {[q["n"] for q in qs][:5]}.. len={len(qs)}')
    for q in qs:
        if sorted(q['opts']) != list('ABCD'): errs.append(f'q{q["n"]} options {sorted(q["opts"])}')
        if not q['exp']: errs.append(f'q{q["n"]} no explanation')
        if not q['stem']: errs.append(f'q{q["n"]} no stem')
        if any(t not in ('一般', '情境', '陷阱') for t in q['tags']): errs.append(f'q{q["n"]} tag {q["tags"]}')
        if '陷阱' in q['tags'] and '陷阱' not in q['exp']: errs.append(f'q{q["n"]} trap without 陷阱 note')
    seq = ''.join(q['ans'] for q in qs)
    if key in SEQ and seq != SEQ[key]:
        diff = [i+1 for i, (a, b) in enumerate(zip(seq, SEQ[key])) if a != b]
        errs.append(f'answer seq mismatch at {diff}')
    sit = sum('情境' in q['tags'] for q in qs); trap = sum('陷阱' in q['tags'] for q in qs)
    if sit < 15: errs.append(f'情境 only {sit}')
    if trap < 10: errs.append(f'陷阱 only {trap}')
    print(f'{key}: 情境 {sit} 陷阱 {trap} 答案分布 {dict(sorted(Counter(seq).items()))} ' + ('OK' if not errs else 'ERR ' + '; '.join(errs)))
    return qs
if __name__ == '__main__':
    for p in sorted(glob.glob(os.path.join(D, 'R*-S*.txt'))): validate(p)
