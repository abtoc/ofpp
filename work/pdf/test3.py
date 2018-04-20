from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table

pdfmetrics.registerFont(TTFont('Gothic','/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'))
psize = portrait(A4)
pwidth, pheight = psize

xmargin = 15.0 * mm
ymargin = 30.0 * mm

c = canvas.Canvas("test3.pdf", pagesize=psize, bottomup=True)
c.setFont('Gothic', 11)
colw = (8.8*mm, 14.5*mm, 36.7*mm, 36.7*mm, 36.7*mm, 50.9*mm)
data = [
    ['yyyy年mm月','','','出勤簿','氏名：','テスト　太郎'],
    ['日','曜日','勤務開始時刻','勤務終了時刻','勤務時間','欠席理由・備考'],
    [ '1','月','10:00','15.00','4.0',''],
    [ '2','火','10:00','15.00','4.0',''],
    [ '3','水','10:00','15.00','4.0',''],
    [ '4','木','10:00','15.00','4.0',''],
    [ '5','金','10:00','15.00','4.0',''],
    [ '6','土','',     '',     '0.0',''],
    [ '7','日','',     '',     '0.0',''],
    [ '8','月','10:00','15.00','4.0',''],
    [ '9','火','10:00','15.00','4.0',''],
    ['10','水','10:00','15.00','4.0',''],
    ['11','木','10:00','15.00','4.0',''],
    ['12','金','10:00','15.00','4.0',''],
    ['13','土','',     '',     '0.0',''],
    ['14','日','',     '',     '0.0',''],
    ['15','月','10:00','15.00','4.0',''],
    ['16','火','10:00','15.00','4.0',''],
    ['17','水','10:00','15.00','4.0',''],
    ['18','木','10:00','15.00','4.0',''],
    ['19','金','10:00','15.00','4.0',''],
    ['20','土','',     '',     '0.0',''],
    ['21','日','',     '',     '0.0',''],
    ['22','月','10:00','15.00','4.0',''],
    ['23','火','10:00','15.00','4.0',''],
    ['24','水','10:00','15.00','4.0',''],
    ['25','木','10:00','15.00','4.0',''],
    ['26','金','10:00','15.00','4.0',''],
    ['27','土','',     '',     '0.0',''],
    ['28','日','',     '',     '0.0',''],
    ['29','月','10:00','15.00','4.0',''],
    ['30','火','10:00','15.00','4.0',''],
    ['31','水','10:00','15.00','4.0',''],
    [''  ,'', '合計勤務時間', '合計勤務日','平均勤務時間',''],
    ['', '',  '92.0','23','4.0',''],
]
table = Table(data, colWidths=colw, rowHeights=6.9*mm)
table.setStyle([
    ('FONT', (0,0), (-1,-1), 'Gothic', 16),
    ('BOX',  (0,0), (-1,-1), 0.5, colors.black),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
    ('ALIGN', (0,1), (0,32), 'RIGHT'),
    ('ALIGN', (1,0), (3,32), 'CENTER'),
    ('ALIGN', (4,0), (4,32), 'RIGHT'),
    ('ALIGN', (2,33),(4,-1), 'RIGHT'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('SPAN', (0,0),(2,0)),
    ('SPAN', (0,33),(1,-1)),
    ('SPAN', (5,33),(5,-1)),
])
table.wrapOn(c, xmargin, ymargin)
table.drawOn(c, xmargin, ymargin)
#c.drawString(xmargin, pheight-ymargin, 'Hello World!')
c.showPage()
c.save()
