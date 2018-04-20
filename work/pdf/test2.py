from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table

pdfmetrics.registerFont(TTFont('Gothic','/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'))
psize = portrait(A4)
pwidth, pheight = psize

xmargin = 10.0 * mm
ymargin = 10.0 * mm
xdd     = xmargin
wdd     = 7.2 * mm
xww     = xdd + wdd
www     = 11.2 * mm
xin     = xww + www
win     = 27.6 * mm
xout    = xin + win
wout    = 27.6 * mm
xval    = xout + wout
wval    = 27.6 * mm
xreason = xval + wval
wreason = pwidth - xmargin - xreason

c = canvas.Canvas("test2.pdf", pagesize=psize, bottomup=False)
c.setFont('Gothic', 11)

y = ymargin
h = 4.5 * mm
w = pwidth - xmargin - xdd
c.rect(xdd, y, w, h, stroke=1, fill=0)
c.drawString(xdd+2,     y+h-2, 'yyyy年mm月')
c.drawString(xout+2,    y+h-2, '出勤簿')
c.drawString(xreason+2, y+h-2, 'テスト　太郎')

y = y + h
c.rect(xdd,       y, wdd,       h, stroke=1, fill=0)
c.rect(xww,       y, www,       h, stroke=1, fill=0)
c.rect(xin,       y, win,  h, stroke=1, fill=0)
c.rect(xout,      y, wout, h, stroke=1, fill=0)
c.rect(xval,      y, wval,    h, stroke=1, fill=0)
c.rect(xreason,   y, wreason,   h, stroke=1, fill=0)
c.drawString(xdd+2, y+h-2, '日')
c.drawString(xww+2, y+h-2, '曜日')
c.drawString(xin+2, y+h-2, '勤務開始時刻')
c.drawString(xout+2, y+h-2, '勤務終了時刻')


c.showPage()
c.save()
