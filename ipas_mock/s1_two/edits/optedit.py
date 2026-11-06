"""依 edits 檔替換 draft 中指定題號的指定選項。edits 格式：『## 題號』後接『(X) 新文字』，未列出的選項不變。
用法：python3 edits/optedit.py draft_R1.txt edits/r1_len.txt"""
import re, sys
d, e = sys.argv[1], sys.argv[2]
txt = open(d, encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=## )', txt)
E = {}
for b in re.split(r'(?m)^(?=## )', open(e, encoding='utf-8').read()):
    if not b.startswith('## '): continue
    n = int(re.match(r'## (\d+)', b).group(1))
    E[n] = dict(re.findall(r'(?m)^\(([A-D])\) (.+)$', b))
out = []; done = []
for b in blocks:
    m = re.match(r'## (\d+) ', b)
    if m and int(m.group(1)) in E:
        n = int(m.group(1))
        for k, v in E[n].items():
            b, c = re.subn(r'(?m)^\(' + k + r'\) .+$', lambda _: f'({k}) {v}', b)
            assert c == 1, (n, k)
        done.append(n)
    out.append(b)
open(d, 'w', encoding='utf-8').write(''.join(out))
print('edited', done, 'missing', sorted(set(E) - set(done)))
