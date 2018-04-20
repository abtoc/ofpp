from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Gothic','/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'))

xmargin = 8.4 * mm
ymargin = 8.8 * mm

c = canvas.Canvas("test1.pdf", pagesize=A4)
c.setFont('Gothic', 16)

c.setLineWidth(0.5)
c.rect(xmargin,ymargin, 48.3*mm, 25.4*mm, stroke=1, fill=0)
c.drawString(48.3*mm, 25.4*mm, 'テストデータ')

c.showPage()
c.save()
