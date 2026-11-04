"""由 pred_v3/S1.txt、S2.txt 產生 data.json 與 ipas_pred_v3.html（以 web/template.html 為基礎）。"""
import os, sys, json
W = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(W); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
data = {}
for s, f in (('s1', 'S1.txt'), ('s2', 'S2.txt')):
    data[s] = [dict(n=q['n'], t=q['tags'], a=q['ans'], q=q['stem'], o=[q['opts'][k] for k in 'ABCD'], e=q['exp'], k=q['topic'])
               for q in parse(os.path.join(D, f))]
json.dump(data, open(os.path.join(W, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sit = sum('情境' in q['t'] for v in data.values() for q in v)
trap = sum('陷阱' in q['t'] for v in data.values() for q in v)
html = open(os.path.join(R, 'web/template.html'), encoding='utf-8').read()
REP = [
    ('<title>iPAS 必考百題模考</title>', '<title>iPAS 考前預測百題 第3版</title>'),
    ('<h1>考前必考 100 題模擬考</h1>', '<h1>考前預測百題（第 3 版）</h1>'),
    ('<p class="lede">依 114 年第 4 次與 115 年第 1～3 次公告試題的考點出現頻率，挑出最常考的觀念編寫。直接點選答案，交卷後自動計分，並顯示每題的正解、詳解與歷屆出處。</p>',
     '<p class="lede">依 114 年第 4 次與 115 年第 1～3 次官方公告試題（共 400 題）的考點統計延伸出題：按各考點的出題比例分配題數，優先選 4 次考試都出現的高頻考點，並加重近期增加的考點（生成式模型、深度學習、AI 風險治理、AI Agent／MCP 等）。每題都是換情境、換問法的全新題目，不含計算題。直接點選答案，交卷後自動計分，並顯示每題的正解與詳解。</p>'),
    ('「歷屆出處」為同考點或同大類的題號', '「考點」後列出的是歷屆同考點或同大類的官方題號'),
    ('<span>建議作答 <b>75</b> 分鐘／科</span>', '<span>建議作答 <b>75</b> 分鐘／科</span>\n    <span>情境題 <b>%d</b>・陷阱題 <b>%d</b>・計算題 <b>0</b></span>' % (sit, trap)),
    ("const KEY = 'ipas-pred100-v2';", "const KEY = 'ipas-pred-v3';"),
    ("'<div class=\"topic\">歷屆出處｜'", "'<div class=\"topic\">考點：'"),
    # 範本的 .result{display:grid} 會蓋過 hidden 屬性，交卷前會出現一個空白框；補上全域規則
    ('</style>', '[hidden]{display:none!important}\n</style>'),
]
for a, b in REP:
    assert html.count(a) == 1, a
    html = html.replace(a, b)
assert html.count('/*DATA*/') == 1
html = html.replace('/*DATA*/', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
open(os.path.join(W, 'ipas_pred_v3.html'), 'w', encoding='utf-8').write(html)
print('ok', {s: len(v) for s, v in data.items()}, '情境', sit, '陷阱', trap, len(html), 'bytes')
