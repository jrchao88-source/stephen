"""由 s1_two/R1.txt、R2.txt 產生 data.json 與 ipas_s1_two.html（以 web/template.html 為基礎；兩個分頁＝第一回、第二回，資料鍵仍用 s1/s2）。"""
import os, sys, json
W = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(W); R = os.path.dirname(D)
sys.path.insert(0, os.path.join(R, 'mock'))
from parse_mock import parse
data = {}
for s, f in (('s1', 'R1.txt'), ('s2', 'R2.txt')):
    data[s] = [dict(n=q['n'], t=q['tags'], a=q['ans'], q=q['stem'], o=[q['opts'][k] for k in 'ABCD'], e=q['exp'], k=q['topic'])
               for q in parse(os.path.join(D, f))]
json.dump(data, open(os.path.join(W, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
cnt = {s: (sum('情境' in q['t'] for q in v), sum('陷阱' in q['t'] for q in v)) for s, v in data.items()}
html = open(os.path.join(R, 'web/template.html'), encoding='utf-8').read()
REP = [
    ('<title>iPAS 必考百題模考</title>', '<title>科目一 情境陷阱百題</title>'),
    ('<div class="eyebrow">iPAS · AI 應用規劃師 · 初級</div>', '<div class="eyebrow">iPAS · AI 應用規劃師 · 初級 · 科目一</div>'),
    ('<h1>考前必考 100 題模擬考</h1>', '<h1>科目一 情境陷阱百題（兩回）</h1>'),
    ('<p class="lede">依 114 年第 4 次與 115 年第 1～3 次公告試題的考點出現頻率，挑出最常考的觀念編寫。直接點選答案，交卷後自動計分，並顯示每題的正解、詳解與歷屆出處。</p>',
     '<p class="lede">只考科目一「人工智慧基礎概論」，分成兩回、每回 50 題全新題目。題目以情境判斷與陷阱選項為主，涵蓋歷屆考點與講義重點（AI 類型判斷、資料處理與統計觀念、機器學習、深度學習、生成式模型、可解釋 AI、治理與隱私、部署維運），不含計算題。每回可單獨交卷，交卷後在每題下方顯示正解與詳解。</p>'),
    ('<span>科目一 人工智慧基礎概論 <b>50</b> 題</span>', '<span>第一回 <b>50</b> 題（情境 <b>%d</b>・陷阱 <b>%d</b>）</span>' % cnt['s1']),
    ('<span>科目二 生成式 AI 應用與規劃 <b>50</b> 題</span>', '<span>第二回 <b>50</b> 題（情境 <b>%d</b>・陷阱 <b>%d</b>）</span>' % cnt['s2']),
    ('<span>每題 <b>2</b> 分，單科滿分 <b>100</b></span>', '<span>每題 <b>2</b> 分，每回滿分 <b>100</b>，可單獨交卷</span>'),
    ('<span>建議作答 <b>75</b> 分鐘／科</span>', '<span>計算題 <b>0</b></span>'),
    ('aria-label="選擇科目"', 'aria-label="選擇回次"'),
    ('data-s="s1">科目一<small', 'data-s="s1">第一回<small'),
    ('data-s="s2">科目二<small', 'data-s="s2">第二回<small'),
    ('題目、答案與詳解由 AI（Claude）依歷屆公告試題的考點編寫，非官方試題；「歷屆出處」為同考點或同大類的題號，供複習參考。實際考試範圍、合格標準請以 iPAS 官方最新簡章為準。作答紀錄只存在你目前使用的瀏覽器中。',
     '題目由 AI（Claude）編寫、非官方試題，合格標準以 iPAS 官方最新簡章為準。題目依歷屆公告試題的考點與學習講義編寫；每題「考點」後列出的是歷屆同考點或同大類的官方題號，供複習參考。作答紀錄只存在你目前使用的瀏覽器中。'),
    ("const KEY = 'ipas-pred100-v2';", "const KEY = 'ipas-s1-two-rounds-v1';"),
    ("'<div class=\"topic\">歷屆出處｜'", "'<div class=\"topic\">考點：'"),
    ('按「重新作答」可清除本科答案再考一次。', '按「重新作答」只會清除本回的答案，另一回不受影響。'),
    ("ask('要清除' + (st.cur === 's1' ? '科目一' : '科目二') + '的所有答案，重新作答嗎？'", "ask('要清除' + (st.cur === 's1' ? '第一回' : '第二回') + '的所有答案，重新作答嗎？'"),
    ('</style>', '[hidden]{display:none!important}\n</style>'),
]
for a, b in REP:
    assert html.count(a) == 1, a
    html = html.replace(a, b)
assert html.count('/*DATA*/') == 1
html = html.replace('/*DATA*/', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
assert '科目二' not in html and '單科' not in html and '本科' not in html
open(os.path.join(W, 'ipas_s1_two.html'), 'w', encoding='utf-8').write(html)
print('ok', {s: len(v) for s, v in data.items()}, cnt, len(html), 'bytes')
