"""由 set3/S1.txt、S2.txt 產生 data.json 與 ipas_exam_set3.html（以 web/template.html 為基礎）。"""
import os, sys, json
W = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(W); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
data = {}
for s, f in (('s1', 'S1.txt'), ('s2', 'S2.txt')):
    data[s] = [dict(n=q['n'], t=q['tags'], a=q['ans'], q=q['stem'], o=[q['opts'][k] for k in 'ABCD'], e=q['exp'], k=q['topic'])
               for q in parse(os.path.join(D, f))]
json.dump(data, open(os.path.join(W, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
html = open(os.path.join(R, 'web/template.html'), encoding='utf-8').read()
REP = [
    ('<title>iPAS 必考百題模考</title>', '<title>iPAS 情境陷阱百題</title>'),
    ('<h1>考前必考 100 題模擬考</h1>', '<h1>情境陷阱百題模擬考</h1>'),
    ('<p class="lede">依 114 年第 4 次與 115 年第 1～3 次公告試題的考點出現頻率，挑出最常考的觀念編寫。直接點選答案，交卷後自動計分，並顯示每題的正解、詳解與歷屆出處。</p>',
     '<p class="lede">全新 100 題，不含任何計算題，以情境題與陷阱題為主：每題都是情境題，大部分同時是陷阱題，詳解會指出陷阱在哪裡。考點依 114 年第 4 次與 115 年第 1～3 次公告試題的出現頻率挑選。直接點選答案，交卷後自動計分，並顯示每題的正解與詳解。</p>'),
    ('「歷屆出處」為同考點或同大類的題號', '「考點」後列出的是歷屆同考點或同大類的題號'),
    ('<span>建議作答 <b>75</b> 分鐘／科</span>', '<span>建議作答 <b>75</b> 分鐘／科</span>\n    <span>情境題 <b>%d</b>・陷阱題 <b>%d</b>・計算題 <b>0</b></span>' % (sum('情境' in q['t'] for v in data.values() for q in v), sum('陷阱' in q['t'] for v in data.values() for q in v))),
    ("const KEY = 'ipas-pred100-v2';", "const KEY = 'ipas-scenario-trap-set3-v1';"),
    ("'<div class=\"topic\">歷屆出處｜'", "'<div class=\"topic\">考點：'"),
]
for a, b in REP:
    assert html.count(a) == 1, a
    html = html.replace(a, b)
assert html.count('/*DATA*/') == 1
html = html.replace('/*DATA*/', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(W, 'ipas_exam_set3.html'), 'w', encoding='utf-8').write(html)
print('ok', {s: len(v) for s, v in data.items()}, len(html))
