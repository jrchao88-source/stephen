import re, sys, importlib.util
def apply(path, edits):
    txt = open(path, encoding='utf-8').read()
    blocks = re.split(r'(?m)^(?=## )', txt)
    out = []
    for b in blocks:
        m = re.match(r'## (\d+) \|', b)
        if m and int(m.group(1)) in edits:
            e = edits[int(m.group(1))]
            lines = b.split('\n')
            for i, l in enumerate(lines):
                mo = re.match(r'^\(([A-D])\) ', l)
                if mo and mo.group(1) in e: lines[i] = f'({mo.group(1)}) ' + e[mo.group(1)]
                if l.startswith('解說：') and 'EXP' in e: lines[i] = '解說：' + e['EXP']
                if l.startswith('解說：') and 'EXP_SUB' in e:
                    for old, new in e['EXP_SUB']:
                        assert old in lines[i], (path, m.group(1), old)
                        lines[i] = lines[i].replace(old, new)
            b = '\n'.join(lines)
        out.append(b)
    open(path, 'w', encoding='utf-8').write(''.join(out))
if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('ed', sys.argv[1]); ed = importlib.util.module_from_spec(spec); spec.loader.exec_module(ed)
    apply(sys.argv[2], ed.EDITS)
