from flask import request, send_file
from app.report import bp
from app.db import db
from app.models.reportModel import Report
from app.models.notPaidCaseModel import NotPaidCase
from app.models.problematicCaseModel import ProblematicCase
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
        return "W bazie nie ma żadnych raportów", 404
    else:
        for report in reports:
            report_json.append(report.json())
        response_data = report_json
        return makeResponse(response_data, 200)


@bp.route('/download/pdf/<id>')
def download(id):
    if not validateId(id):
        return "Plik o danym id nie istnieje", 404
    
    report = Report.query.filter_by(id=id).first()
    path=os.path.join(
        os.getcwd(), 
        Config.REPORT_FOLDER,
        report.file_name,
        "pdf"
    )
    return send_file(path, as_attachment=True)

@bp.route('/download/csv/<id>')
def download(id):
    if not validateId(id):
        return "Plik o danym id nie istnieje", 404
    
    report = Report.query.filter_by(id=id).first()
    path=os.path.join(
        os.getcwd(), 
        Config.REPORT_FOLDER,
        report.file_name,
        "csv"
    )
    return send_file(path, as_attachment=True)


@bp.route('/add', methods=["POST"])
def create():
    data = getRequestData(request)

    if not allElementsInList(Report.attr, data):
        return "Zapytanie nie zawiera wszystkich wymaganych wartości", 400

    if not validateDate(data['start_period']) and not validateDate(data['end_peroid']):
        return "Podane formaty dat nie są poprawne", 404
    
    start_period = datetime.strptime(data['start_period'], '%Y-%m-%dT%H:%M:%SZ')
    end_peroid = datetime.strptime(data['end_peroid'], '%Y-%m-%dT%H:%M:%SZ')
    
    notPaidCases = NotPaidCase.query.filter(
        NotPaidCase.detect_time <= end_peroid, 
        NotPaidCase.detect_time>= start_period
    ).all()
    
    problematicCases = ProblematicCase.query.filter(
        ProblematicCase.detect_time >= start_period, 
        ProblematicCase.detect_time <= end_peroid
    ).all()

    filename = start_period.strftime("%Y%m%d")+"-"+end_peroid.strftime("%Y%m%d")
    report = Report(start_period, end_peroid, filename)
    db.session.add(report)
    db.session.commit()

    pdfFilename = filename + '_' + getUuid() + '.pdf'
    generatePDF(pdfFilename, start_period, end_peroid, notPaidCases, problematicCases)

    xlsxFilename = filename + '_' + getUuid() + '.xlsx'
    generateXLSX(filename, notPaidCases, problematicCases)
        
    data = {"xslx_name": xlsxFilename, "pdf_name": pdfFilename}
    return makeResponse(data, 200)