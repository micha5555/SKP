from app.report import bp
from app.db import db
from app.models.reportModel import Report
from app.models.notPaidCaseModel import NotPaidCase
from app.models.problematicCaseModel import ProblematicCase
from flask import request, make_response, send_file
from app.validators import *
from app.extensions import *
from datetime import datetime
from app.generators import *
from config import Config


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


@bp.route('/download/<id>')
def download(id):
    if not validateId(id):
        return {"error": "Element does not exists"}, 404
    report = Report.query.filter_by(id=id).first()
    path=os.path.join(
            os.getcwd(), 
            Config.REPORT_FOLDER,report.file_name,"pdf")
    return send_file(path, as_attachment=True) #poprawiłam ścieżke ale czy my to chcemy zipować? albo potrzebujemy 2 routów 


@bp.route('/add', methods=["POST"])
def create():
    if request.method == "POST":
        data = getRequestData()
        if data is None:
            return {"error": "request is null"}, 404

        if not validateDate(data['start_peroid']) and not validateDate(data['end_peroid']):
            return {"error": "dates not accepted"}, 404
        
        start_peroid = datetime.strptime(data['start_peroid'], '%Y-%m-%dT%H:%M:%SZ')
        end_peroid = datetime.strptime(data['end_peroid'], '%Y-%m-%dT%H:%M:%SZ')
        
        notPaidCases = NotPaidCase.query.filter(
            NotPaidCase.detect_time <= end_peroid, 
            NotPaidCase.detect_time>= start_peroid
        ).all()
        
        problematicCases = ProblematicCase.query.filter(
            ProblematicCase.detect_time >= start_peroid, 
            ProblematicCase.detect_time <= end_peroid
        ).all()

        filename = start_peroid.strftime("%d%m%Y")+"-"+end_peroid.strftime("%d%m%Y")
        description = data['start_peroid']+":"+data['end_peroid']
        report = Report(filename, description)

        pdfFilename = filename+'.pdf'
        generatePDF()

        xlsxFilename = filename+'.xlsx'
        generateXLSX(filename, notPaidCases, problematicCases)
        
        return {"xslx_name": xlsxFilename, "pdf_name": pdfFilename}, 200