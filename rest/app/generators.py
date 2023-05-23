import xlsxwriter
from fpdf import FPDF
from config import Config
import os

def generateXLSX(filename,notPaidCases,problematicCases):
    xlsxDest = os.path.join(
        os.getcwd(),
        Config.REPORT_FOLDER,
        filename + '.xlsx')
    xlsx = xlsxwriter.Workbook(xlsxDest)
    worksheet = xlsx.add_worksheet("Not paid cases")
    row = 0
    col = 0
    worksheet.write(row, col, "id")
    worksheet.write(row, col+1, "registration")
    worksheet.write(row, col+2, "detect time")
    worksheet.write(row, col+3, "localization")
    worksheet.write(row, col+4, "image name")
    row += 1
    for notPaid in notPaidCases:
        worksheet.write(row, col, notPaid.id)
        worksheet.write(row, col+1, notPaid.registration_plate)
        worksheet.write(row, col+2, notPaid.detect_time)
        worksheet.write(row, col+3, notPaid.localization)
        worksheet.write(row, col+4, notPaid.image)
        row += 1
    worksheet = xlsx.add_worksheet("Problematic cases")
    row = 0
    col = 0
    worksheet.write(row, col, "id")
    worksheet.write(row, col+1, "registration")
    worksheet.write(row, col+2, "detect time")
    worksheet.write(row, col+3, "localization")
    worksheet.write(row, col+4, "image name")
    worksheet.write(row, col+5, "edit time")
    worksheet.write(row, col+6, "probability")
    worksheet.write(row, col+7, "status")
    worksheet.write(row, col+8, "correction")
    row += 1
    for problematic in problematicCases:
        worksheet.write(row, col, problematic.id)
        worksheet.write(row, col+1, problematic.registration_plate)
        worksheet.write(row, col+2, problematic.detect_time)
        worksheet.write(row, col+3, problematic.localization)
        worksheet.write(row, col+4, problematic.image)
        worksheet.write(
            row, col+5, problematic.administration_edit_time)
        worksheet.write(row, col+6, problematic.probability)
        worksheet.write(row, col+7, problematic.status)
        worksheet.write(row, col+8, problematic.correction)
        row += 1
    xlsx.close()

def generatePDF(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 20)
    txt = "SKP Report from: " +data['start_peroid'] +" to: "+data['end_peroid']
    pdf.cell(w=0, h=10, txt=txt, ln=1)
    pdf.set_font('Arial', '', 16)
    txt = "Total number of not paid cases: "+str(len(notPaidCases))
    pdf.cell(w=0, h=10, txt=txt, ln=1)
    txt = "Total number of problematic cases: "+str(len(problematicCases))
    pdf.cell(w=0, h=10, txt=txt, ln=1)
    current_date = start_date
    while current_date <= end_date:
        txt = "Date: "+current_date.strftime("%d/%m/%Y")
        pdf.cell(w=0, h=10, txt=txt, ln=1)
        notPaidCasesForDay = NotPaidCase.query.filter(
        NotPaidCase.detect_time == current_date).all()
        txt = "Number of not paid cases :"+str(len(notPaidCasesForDay))
        pdf.cell(w=0, h=10, txt=txt, ln=1)
        problematicCasesForDay = ProblematicCase.query.filter(
        NotPaidCase.detect_time == current_date).all()
        txt = "Number of problematic cases: "+str(len(problematicCases))
        pdf.cell(w=0, h=10, txt=txt, ln=1)
    pdfDest=os.path.join(
        os.getcwd(), 
        Config.REPORT_FOLDER, 
        filename + '.pdf')
    pdf.output(pdfDest,'F')