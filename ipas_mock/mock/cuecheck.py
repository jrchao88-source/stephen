import sys
from lenstat import parse, L
for f in sys.argv[1:]:
    qs=parse(f); c=w=0; ranks=[0,0,0,0]; r2=[]
    for q in qs:
        lens={k:L(v) for k,v in q['opts'].items()}
        a=lens[q['ans']]
        # rank with ties counted against the answer (ties => better rank)
        r=sum(1 for k,v in lens.items() if k!=q['ans'] and v>a)
        ranks[r]+=1
        if r==1: r2.append(q['n'])
        for k,v in q['opts'].items():
            has=('因為' in v or '所以' in v)
            if k==q['ans']: c+=has
            else: w+=has
    print(f, '正解長度排名[最長,第2,第3,最短]:', ranks, f'| 含因為/所以 正解 {c}/50 錯誤 {w}/150', '| 第2長題號', r2)
