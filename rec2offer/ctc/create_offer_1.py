from django.http import HttpResponse
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
import os

 
def create_offer(data):
    try:
        name = data['name']
        designation  = data['designation']
        description = data['description']
        ctc = data['ctc']

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{name}_{designation}.pdf"'
        
        pm = round((int(ctc)/12),2)
        basic = round(((int(pm) * (40 / 100))*12),2)
        epf = round( (basic * (12 / 100)),2 )
        hra = round((basic * (40 / 100)) ,2)
        company = round((basic * (12 / 100)) ,2)
        pt = round(((150*12 if int(pm) < 21000 else 200*12)),2)
        food_card = round((1100.0*12 if int(ctc) < 500000 else 3000.0*12),2)
        provident_fund = round((basic * (12 / 100)),2)
        bonus = 0.00
        project_allowance = 0.00
        location_allowance = 0.00
        gratuity = round((basic * (4.83 / 100)),2)
        insurance = 0.00
        flexi_basket = 0.00
        spl_allowance = round((pm*12 - (basic + hra + food_card + provident_fund + bonus + gratuity )),2)
        performance_pay = 0.00
        total_earnings = round((basic + hra + spl_allowance + food_card + provident_fund + bonus + project_allowance + location_allowance
                            + gratuity + insurance + flexi_basket + performance_pay),2)
        total_deductions = round((epf + company + pt),2)
        data = [
            ['Earnings','', 'Deductions' ],
            ['Basic', basic, 'EPF', epf],
            ['HRA',hra,'COMPANY',company],
            ['SPL_ALLOWANCE',spl_allowance,'PT',pt],
            ['FOOD CARD',food_card,'',''],
            ['PROVIDENT FUND',provident_fund,'',''],
            ['BONUS',bonus,'',''],
            ['PROJECT ALLOWANCE',project_allowance,'',''],
            ['LOCATION ALLOWANCE',location_allowance,'',''],
            ['GRATUITY',gratuity,'',''],
            ['INSURANCE',insurance,'',''],
            ['FLEXI BASKET',flexi_basket,'',''],
            ['PERFORMANCE PAY',performance_pay,'',''],
            ['TOTAL EARNINGS',total_earnings,'TOTAL DEDUCTIONS',total_deductions]
        ]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        file_name = os.path.join(base_dir, f"offer_letters\{name}.pdf")
        # pdf = SimpleDocTemplate(file_name, pagesize=A4)
        pdf = SimpleDocTemplate(response, pagesize=A4)

        table = Table(data)
        style = TableStyle([
            ('TEXTCOLOR',(0,0),(-1,0),colors.black),
            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('ALIGN',(0,1),(-1,-1),'LEFT'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,1), (-1,-1), 15),
            ('RIGHTPADDING', (0,1), (-1,-1), 15),
            ('TOPPADDING', (0,-1), (-1,-1), 8),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('LINEBEFORE',(0,1),(1,-1),2,colors.black),
            ('LINEAFTER',(0,1),(1,-1),2,colors.black),
            ('LINEBEFORE',(-1,1),(-1,-1),2,colors.black),
            ('LINEABOVE',(0,1),(-1,1),2,colors.black),
            ('LINEABOVE',(0,-1),(-1,-1),2,colors.black),
        ])
        table.setStyle(style)
        elems = [
            Paragraph('Offer Letter', getSampleStyleSheet()['Title']),
            Spacer(1 * cm, 1 * cm),
            Paragraph(f'Name: {name}'),
            Spacer(1, 1),
            Paragraph(f'Designation: {designation}'),
            Spacer(1 * cm, 1 * cm),
            Paragraph(description),
            Spacer(1 * cm, 1 * cm),
            
            table
        ]
        pdf.build(elems)
        # return {"status":"created successfully","path":file_name}
        return response
    except Exception as e:
        print(e)
        return False