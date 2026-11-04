"""在舊題語料中搜尋關鍵字，確認新角度未被用過。用法：python3 kw.py 關鍵字1 關鍵字2 ...（每個關鍵字分開列出命中題）"""
import sys, os, glob, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mock'))
from parse_mock import parse
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
items = []
for q in json.load(open(os.path.join(R, 'ref/official_junior_questions.json'), encoding='utf-8')):
    items.append((f"官方{q['exam']}-{q['subject']}-{q['n']}", q['text']))
for f in sorted(glob.glob(R+'/mock/R*-S*.txt')+glob.glob(R+'/pred/P-S*.txt')+glob.glob(R+'/pred/backup_v*/P-S*.txt')+glob.glob(R+'/set3/S[12].txt')):
    for q in parse(f): items.append((os.path.relpath(f, R)+'#'+str(q['n']), q['stem']+' ▶'+q['opts'][q['ans']]))
for k in sys.argv[1:]:
    hits = [(n, t) for n, t in items if k in t]
    print(f'== {k}: {len(hits)}')
    for n, t in hits[:6]: print('  ', n, t.replace('\n', '')[:150])
