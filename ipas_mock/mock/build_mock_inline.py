import os, re, sys
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from parse_mock import validate

S = sys.argv[1]
ROUNDS = [int(x) for x in sys.argv[2].split(',')]
OUTDIR = sys.argv[3]
ADV = {4, 5, 6}  # rounds rewritten at higher difficulty
pdfmetrics.registerFont(TTFont('TC', os.path.join(S, 'fonts/NotoTC-Regular.ttf')))
pdfmetrics.registerFont(TTFont('TCB', os.path.join(S, 'fonts/NotoTC-Bold.ttf')))
addMapping('TC', 0, 0, 'TC'); addMapping('TC', 1, 0, 'TCB'); addMapping('TC', 0, 1, 'TC'); addMapping('TC', 1, 1, 'TCB')

INK = colors.HexColor('#1f2933'); MUTED = colors.HexColor('#5f6b7a'); ACC = colors.HexColor('#1d4ed8')
BOXBG = colors.HexColor('#f3f6fb'); BOXLN = colors.HexColor('#c9d4e5'); TRAP = colors.HexColor('#b45309')
def st(name, **kw):
    base = dict(fontName='TC', fontSize=10.5, leading=16, textColor=INK, wordWrap='CJK'); base.update(kw)
    return ParagraphStyle(name, **base)
sTitle = st('t', fontName='TCB', fontSize=24, leading=34, alignment=TA_CENTER)
sSub = st('s', fontSize=13, leading=20, alignment=TA_CENTER, textColor=MUTED)
sH1 = st('h1', fontName='TCB', fontSize=17, leading=24, spaceAfter=4, textColor=ACC)
sH2 = st('h2', fontName='TCB', fontSize=13, leading=19, spaceBefore=4, spaceAfter=4)
sBody = st('b'); sSmall = st('sm', fontSize=9, leading=13.5, textColor=MUTED)
sQ = st('q', leftIndent=20, firstLineIndent=-20, spaceBefore=2)
sOpt = st('o', leftIndent=40, firstLineIndent=-20, leading=15.5)
sQs = st('qs', fontSize=9.5, leading=14, leftIndent=20, firstLineIndent=-20, textColor=MUTED)
sOpts = st('os', fontSize=9.5, leading=14, leftIndent=40, firstLineIndent=-20, textColor=MUTED)
sAns = st('a', fontSize=10, leading=15.5)
sToc0 = st('toc0', fontName='TCB', fontSize=11.5, leading=20); sToc1 = st('toc1', fontSize=10.5, leading=17, leftIndent=14)
SUBJ = {1: '科目一：人工智慧基礎概論', 2: '科目二：生成式AI應用與規劃'}
NUM = '零一二三四五六'

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class Doc(BaseDocTemplate):
    def afterFlowable(self, f):
        if hasattr(f, 'toc_level'):
            key = 'k%d' % id(f)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f.toc_text, key, level=f.toc_level, closed=False)
            self.notify('TOCEntry', (f.toc_level, f.toc_text, self.page, key))
def heading(text, style, level):
    p = Paragraph(text, style); p.toc_level = level; p.toc_text = re.sub('<[^>]+>', '', text); return p

def build(r):
    data = {s: validate(os.path.join(D, f'R{r}-S{s}.txt')) for s in (1, 2)}
    out = os.path.join(OUTDIR, f'AI應用規劃師_初級_模擬試題_第{r}回_{'進階版_' if r in ADV else ''}逐題詳解版.pdf')
    def footer(c, doc):
        c.saveState(); c.setFont('TC', 8); c.setFillColor(MUTED)
        c.drawString(18*mm, 10*mm, f'iPAS AI應用規劃師（初級）模擬試題 第{NUM[r]}回｜AI 自編題目，非官方試題，僅供練習')
        c.drawRightString(A4[0] - 18*mm, 10*mm, str(doc.page)); c.restoreState()
    doc = Doc(out, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=18*mm,
              title=f'iPAS AI應用規劃師（初級）模擬試題 第{NUM[r]}回' + ('（進階版）' if r in ADV else '') + '（含詳解）', author='出題：Claude（AI）')
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)], onPage=footer)])
    CW = doc.width - 12
    story = [Spacer(1, 45*mm), Paragraph('iPAS 經濟部產業人才能力鑑定', sSub), Spacer(1, 4*mm),
             Paragraph(f'AI應用規劃師（初級）<br/>模擬試題　第{NUM[r]}回' + ('（進階版）' if r in ADV else ''), sTitle), Spacer(1, 6*mm),
             Paragraph('科目一 50 題＋科目二 50 題｜附答案與逐題詳解', sSub), Spacer(1, 14*mm)]
    rows = []
    for s in (1, 2):
        qs = data[s]
        sit = sum('情境' in q['tags'] for q in qs); trap = sum('陷阱' in q['tags'] for q in qs)
        rows.append([Paragraph(SUBJ[s], sBody), Paragraph(f'單選題 50 題｜情境題 {sit} 題｜陷阱題 {trap} 題｜建議作答時間 75 分鐘', sBody)])
    rows.append([Paragraph('出題說明', sBody), Paragraph(('依 iPAS 官方公告的歷屆初級試題考點，由 AI（Claude）自行出題，<b>非官方試題</b>。<b>進階版難度高於官方初級試題</b>：加入多概念綜合情境、組合判斷、兩步驟以上的計算，以及少數銜接中級的延伸觀念。' if r in ADV else '依 iPAS 官方公告的歷屆初級試題考點與題型風格，由 AI（Claude）自行出題，<b>非官方試題</b>，難度比照初級。'), sBody)])
    t = Table(rows, colWidths=[54*mm, CW - 54*mm])
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, BOXLN), ('BACKGROUND', (0, 0), (0, -1), BOXBG), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    story += [t, Spacer(1, 10*mm)]
    for n in ['<b>使用方式：</b>每一題的答案與詳解，都放在該題下方約 3.5 公分留白之後，並以虛線「▼ 作答後再往下看答案 ▼」隔開。作答時，請用手或一張紙遮住虛線以下的部分，選好答案後再移開對照。也可以整份作答完再一起對答案，檔案最後附有「答案速查」方便計分。每題 2 分，70 分及格。',
              '<b>題型標示：</b>為了不影響作答，題型（情境題、陷阱題）只標示在答案欄中。陷阱題會說明陷阱在哪裡，常見的陷阱包括否定詞（何者錯誤、不是）、絕對用語（一定、保證、完全）、名稱相近的概念，以及計算時的單位或分母。',
              '<b>注意：</b>題目與詳解由 AI 撰寫，已盡力確保正確；涉及產品功能與法規的內容，以官方最新資訊為準。']:
        story += [Paragraph(n, sBody), Spacer(1, 3*mm)]
    story.append(PageBreak())
    story.append(Paragraph('目錄', sH1)); toc = TableOfContents(); toc.levelStyles = [sToc0, sToc1]
    story += [toc, PageBreak()]
    # questions with answer below each (gap for covering)
    GAP = 35*mm
    for s in (1, 2):
        story.append(heading(f'{SUBJ[s]}　試題與詳解', sH1, 0))
        story.append(Paragraph('單選題，共 50 題，每題 2 分。每題下方留白後附答案與詳解，作答時請先用手或紙遮住留白以下的部分。', sSmall)); story.append(Spacer(1, 4*mm))
        for q in data[s]:
            kinds = [t for t in q['tags'] if t != '一般']
            label = '、'.join(k + '題' for k in kinds) if kinds else '一般題'
            block = [Paragraph(f'<b>{q["n"]}.</b> {esc(q["stem"]).replace(chr(10), "<br/>")}', sQ)]
            for L in 'ABCD': block.append(Paragraph(f'({L}) {esc(q["opts"][L])}', sOpt))
            block.append(Spacer(1, GAP))
            cut = Table([[Paragraph('▼ 作答後再往下看答案 ▼', st('cut', fontSize=8, leading=10, alignment=TA_CENTER, textColor=MUTED))]], colWidths=[CW - 8])
            cut.setStyle(TableStyle([('LINEABOVE', (0, 0), (-1, 0), 0.6, BOXLN, 1, (3, 3)), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
            cut.hAlign = 'RIGHT'
            e = esc(q['exp'])
            e = re.sub(r'(陷阱：)', r'<font color="#b45309"><b>\1</b></font>', e)
            box = Table([[Paragraph(f'<b>答案：<font color="#1d4ed8">{q["ans"]}</font></b>　<font color="#5f6b7a">［{label}］</font><br/><b>詳解：</b>{e}', sAns)]], colWidths=[CW - 8])
            box.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BOXBG), ('BOX', (0, 0), (-1, -1), 0.6, BOXLN),
                                     ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                                     ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
            box.hAlign = 'RIGHT'
            sep = Table([['']], colWidths=[CW + 12], rowHeights=[1])
            sep.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1.2, colors.HexColor('#94a3b8'))]))
            block += [cut, Spacer(1, 2), box, Spacer(1, 6), sep, Spacer(1, 8)]
            story.append(KeepTogether(block))
        story.append(PageBreak())
    # answer key
    story.append(heading('答案速查（計分用）', sH1, 0))
    for s in (1, 2):
        qs = data[s]; story.append(Paragraph(f'<b>{SUBJ[s]}</b>', sBody)); story.append(Spacer(1, 1*mm))
        rows = []
        for rr in range(5):
            rows.append([Paragraph(f'<b>{rr*10+i+1}</b>', st('k', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=MUTED)) for i in range(10)])
            rows.append([Paragraph(f'<b>{qs[rr*10+i]["ans"]}</b>', st('k2', fontName='TCB', fontSize=10, leading=13, alignment=TA_CENTER, textColor=ACC)) for i in range(10)])
        kt = Table(rows, colWidths=[CW/10]*10)
        ts = [('GRID', (0, 0), (-1, -1), 0.4, BOXLN), ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]
        for k in range(0, 10, 2): ts.append(('BACKGROUND', (0, k), (-1, k), BOXBG))
        kt.setStyle(TableStyle(ts)); story += [kt, Spacer(1, 6*mm)]
    doc.multiBuild(story)
    return out

for r in ROUNDS:
    print(build(r))
