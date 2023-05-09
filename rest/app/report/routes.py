from app.report import bp
from app.db import db
from app.models.reportModel import Report
from app.models.notPaidCaseModel import NotPaidCase
from app.models.problematicCaseModel import ProblematicCase
from flask import request, make_response, send_file
import json
from datetime import datetime
from fpdf import FPDF
import xlsxwriter


@bp.route('/', methods=["GET"])
def get():
    reports = Report.query.order_by(Report.date.asc()).all()
    report_json = []
    if reports is None:
        return {"error": "No report in DB"}, 404
    else:
        for report in reports:
            report_json.append(report.json())
        response_data = report_json
        response = make_response(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response, 200


@bp.route('/download/<int:id>')
def download():
    report = Report.query.filter_by(id=id).first()
    # prawdopodobnie będzie problem ze ścieżką,jak coś nie działa to pewnie to
    return send_file(report.file_name, as_attachment=True)


@bp.route('/add', methods=["POST"])
def create():
    if request.method == "POST":
        # walidacja dat i jakie nazwy na razie daje start_peroid i end_peroid i datetime z tego trzeba utworzyć
        print(" 0")
        data = request.get_json()
        if data is None:
            return {"error": "json is null"}, 404
        print(" 1")
        start_peroid = datetime.strptime(data['start_peroid'], '%Y-%m-%dT%H:%M:%SZ')
        end_peroid = datetime.strptime(data['end_peroid'], '%Y-%m-%dT%H:%M:%SZ')
        print(start_peroid)
        notPaidCases = NotPaidCase.query.filter(
         NotPaidCase.detect_time <= end_peroid,NotPaidCase.detect_time>= start_peroid).all()
        problematicCases = ProblematicCase.query.filter(
            ProblematicCase.detect_time >= start_peroid, ProblematicCase.detect_time <= end_peroid).all()

        filename = start_peroid.strftime("%d%m%Y")+"-"+end_peroid.strftime("%d%m%Y")# Pewnie zmiana filename
        description = data['start_peroid']+":"+data['end_peroid']
        report = Report(filename, description)
        print("generate pdf")
        # generowanie PDF
        pdf = FPDF()
        pdf.add_page()
        pdfFilename = filename+'.pdf'
        pdf.set_font('Arial', '', 16)
        txt = "Number of not paid cases: "+str(len(notPaidCases))
        pdf.cell(w=0, h=10, txt=txt, ln=1)
        txt = "Number of problematic cases: "+str(len(problematicCases))
        pdf.cell(w=0, h=10, txt=txt, ln=1)
        pdfDest='reports/'+pdfFilename
        pdf.output(pdfDest,'F')

        # generowanie XLSX
        print("generate xlsx")
        xlsxFilename = filename+'.xlsx'
        xlsxDest='reports/'+xlsxFilename
        xlsx = xlsxwriter.Workbook(xlsxDest)
        worksheet = xlsx.add_worksheet("Not paid cases")
        row = 0
        col = 0
        worksheet.write(row, col, "id")
        worksheet.write(row, col+1, "registration")
        worksheet.write(row, col+2, "detect time")
        worksheet.write(row, col+3, "localization")
        worksheet.write(row, col+4, "image name")
        row+=1
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
        row+=1
        for problematic in problematicCases:
            worksheet.write(row, col, problematic.id)
            worksheet.write(row, col+1, problematic.registration_plate)
            worksheet.write(row, col+2, problematic.detect_time)
            worksheet.write(row, col+3, problematic.localization)
            worksheet.write(row, col+4, problematic.image)
            worksheet.write(row, col+5, problematic.administration_edit_time)
            worksheet.write(row, col+6, problematic.probability)
            worksheet.write(row, col+7, problematic.status)
            worksheet.write(row, col+8, problematic.correction)
            row += 1
        xlsx.close()
        return {"xslx_name": xlsxFilename, "pdf_name": pdfFilename}, 200
