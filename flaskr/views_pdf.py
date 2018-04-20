from flask                        import Blueprint
from flask                        import request, make_response, abort, flash
from reportlab.pdfgen             import canvas
from reportlab.lib                import colors
from reportlab.lib.pagesizes      import A4, portrait
from reportlab.lib.units          import mm
from reportlab.pdfbase            import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts    import TTFont
from reportlab.platypus           import Table
from io                           import BytesIO
from flaskr                       import db
from flaskr.models                import Person,WorkRec
from datetime                     import datetime
from dateutil.relativedelta       import relativedelta

pdfmetrics.registerFont(TTFont('Gothic','/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'))
bp = Blueprint('pdf', __name__, url_prefix="/pdf")

def make_items(id,yymm):
    person = Person.query.filter_by(id=id).first()
    if person == None:
        return None
    yy     = int(yymm[:4])
    mm     = int(yymm[4:])
    ym     = '{yy}年{mm}月'.format(yy=yy,mm=mm)
    first  = datetime(yy, mm, 1) 
    sum    = 0.0
    cnt    = 0
    items  = []
    item   = [ym, '', '', '出勤簿','氏名：', person.name]
    items.append(item) 
    item   = ['日', '曜日', '勤務開始時刻', '勤務終了時刻','勤務時間', '欠席理由・備考']
    items.append(item)
    for dd in range(1,32):
        if mm != first.month:
            item = ['','','','','','']
        else:
            item = []
            item.append(str(dd))
            item.append(first.strftime('%a'))
            workrec = WorkRec.query.filter_by(person_id=id, yymm=yymm, dd=dd).first()
            if workrec == None:
                item.append('')
                item.append('')
                item.append('0.0')
                item.append('')
            else:
                item.append(workrec.work_in)
                item.append(workrec.work_out)
                if workrec.value == None:
                    item.append('0.0')
                else:
                    item.append(str(workrec.value))
                item.append(workrec.reason)
                if (workrec.value != None) and (workrec.value != 0.0):
                  sum = sum + workrec.value
                  cnt = cnt + 1
        items.append(item)
        first = first + relativedelta(days=1)
    item = ['','','合計勤務時間','合計勤務日','平均勤務時間','']
    items.append(item)
    if cnt > 0:
        avg = round(sum / cnt, 1)
    else:
        avg = 0.0
    item = ['','', str(sum), str(cnt), str(avg), '']
    items.append(item)
    return items

def make_pdf(items):
    colw   = (8.8*mm, 14.5*mm, 36.7*mm, 36.7*mm, 36.7*mm, 50.9*mm)
    table  = Table(items, colWidths=colw, rowHeights=6.9*mm)
    table.setStyle([
        ('FONT', (0,0), (-1,-1), 'Gothic', 16),
        ('BOX',  (0,1), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,1), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,1), (0,32), 'RIGHT'),
        ('ALIGN', (1,0), (3,32), 'CENTER'),
        ('ALIGN', (4,0), (4,32), 'RIGHT'),
        ('ALIGN', (2,33),(4,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (0,0),(2,0)),
        ('SPAN', (0,33),(1,-1)),
        ('SPAN', (5,33),(5,-1)),
    ])

    output = BytesIO()
    psize  = portrait(A4)
    p = canvas.Canvas(output, pagesize=psize, bottomup=True)
    #p.setFont('Gothic')
    table.wrapOn(p, 15.0*mm, 30.0*mm)
    table.drawOn(p, 15.0*mm, 30.0*mm)
    p.showPage()
    p.save()

    result = output.getvalue()
    output.close()
    return result

@bp.route('/<id>/<yymm>')
def print_pdf(id,yymm):
    items = make_items(id, yymm)
    if items == None:
        abort(404)
    response = make_response(make_pdf(items))
    response.mimetype = 'application/pdf'
    return response
