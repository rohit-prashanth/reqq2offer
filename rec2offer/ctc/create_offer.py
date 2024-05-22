from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter,A4
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from rec2offer.settings import BASE_DIR

def create_offer(data):
    try:
        # List of Lists
        print(f"data: {data}")
        name = data['name']
        name_string = f'Name: {name}'
        designation = data['designation']
        designation_string = f'Designation: {designation}'
        ctc = data['ctc']

        pm = int(ctc)/12

        basic = (int(pm) * (40 / 100))*12
        epf = basic * (12 / 100)
        hra = basic * (40 / 100)
        company = basic * (12 / 100)
        pt = (150*12 if int(pm) < 21000 else 200*12)
        food_card = (1100.0*12 if int(ctc) < 500000 else 3000.0*12)
        provident_fund = basic * (12 / 100)
        bonus = 0.00
        project_allowance = 0.00
        location_allowance = 0.00
        gratuity = basic * (4.83 / 100)
        insurance = 0.00
        flexi_basket = 0.00
        spl_allowance = (pm*12 - (basic + hra + food_card + provident_fund + bonus + gratuity ))
        performance_pay = 0.00

        total_earnings = (basic + hra + spl_allowance + food_card + provident_fund + bonus + project_allowance + location_allowance
                            + gratuity + insurance + flexi_basket + performance_pay)
        total_deductions = (epf + company + pt)

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

        print(f"total_deductions: {total_deductions}")
        print(f"{BASE_DIR}")
        base_dir = BASE_DIR.joinpath(name)
        print("base_dir:",base_dir)
        fileName = base_dir + f"\{name}.pdf"

        print(f"fileName: {fileName}")

        pdf = SimpleDocTemplate(
            fileName,
            pagesize=A4
        )


        table = Table(data)

        # add style


        style = TableStyle([
            # ('BACKGROUND', (0,0), (3,0), colors.green),
            ('TEXTCOLOR',(0,0),(-1,0),colors.black),

            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('ALIGN',(0,1),(-1,-1),'LEFT'),
            
            

            # ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),

            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,1), (-1,-1), 15),
            ('RIGHTPADDING', (0,1), (-1,-1), 15),
            ('TOPPADDING', (0,-1), (-1,-1), 8),

            
            # ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ])
        table.setStyle(style)

        # 2) Alternate backgroud color
        # rowNumb = len(data)
        # for i in range(1, rowNumb):
        #     if i % 2 == 0:
        #         bc = colors.burlywood
        #     else:
        #         bc = colors.beige
            
        #     ts = TableStyle(
        #         [('BACKGROUND', (0,i),(-1,i), bc)]
        #     )
        #     table.setStyle(ts)

        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,0),(-1,-1),2,colors.black),

            ('LINEBEFORE',(0,1),(1,-1),2,colors.black),
            ('LINEAFTER',(0,1),(1,-1),2,colors.black),
            ('LINEBEFORE',(-1,1),(-1,-1),2,colors.black),
            ('LINEABOVE',(0,1),(-1,1),2,colors.black),
            ('LINEABOVE',(0,-1),(-1,-1),2,colors.black),

            # ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )
        table.setStyle(ts)

        elems = []
        elems.append(table)

        # pdf.build(elems)

        styles = getSampleStyleSheet()

        flowables = [
            Paragraph('Offer Letter', styles['Title']),
            Spacer(1 * cm, 1 * cm),
            Paragraph(name_string),
            Spacer(1, 1),
            Paragraph(designation_string),
            Spacer(1 * cm, 1 * cm),
            table
            

        ]

        def onFirstPage(canvas, document):
            canvas.drawCentredString(100, 100, 'Text drawn with onFirstPage')

        # pdf.build(flowables, onFirstPage=onFirstPage)
        pdf.build(flowables)

        return True
    except:
        return False