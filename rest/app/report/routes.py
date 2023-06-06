from flask import request, send_file, send_from_directory
from app.report import bp
from app.db import db
from app.models.reportModel import Report
from app.models.notPaidCaseModel import NotPaidCase
from app.models.problematicCaseModel import ProblematicCase
from app.validators import *
from app.extensions import *
from app.auth import tokenAdminRequire
from datetime import datetime
from app.generators import *
from config import Config
import zipfile


@bp.route('/', methods=["GET"])
@tokenAdminRequire
def get(curr_user):
    reports = Report.query.order_by(Report.creation_date.asc()).all()
    report_json = []
    if reports is None:
        return "W bazie nie ma żadnych raportów", 404
    
    for report in reports:
        report_json.append(report.json())
    response_data = report_json
    return makeResponse(response_data, 200)


@bp.route('/download/pdf/<id>')
@tokenAdminRequire
def download_pdf(curr_user, id):

    if not validateId(id):
        return "Plik o danym id nie istnieje", 404
    
    report = Report.query.filter_by(id=id).first()
    path_pdf=os.path.join(
        os.getcwd(), 
        Config.REPORT_FOLDER,
        report.filename + ".pdf"
    )
    return send_file(path_pdf, as_attachment=True)


@bp.route('/download/xlsx/<id>')
@tokenAdminRequire
def download_xlsx(curr_user, id):

    if not validateId(id):
        return "Plik o danym id nie istnieje", 404
    
    report = Report.query.filter_by(id=id).first()
    path_xlsx=os.path.join(
        os.getcwd(), 
        Config.REPORT_FOLDER,
        report.filename + ".xlsx"
    )
    return send_file(path_xlsx, as_attachment=True)

@bp.route('/add', methods=["POST"])
@tokenAdminRequire
def create(curr_user):
    data = getRequestData(request)

    if not allElementsInList(Report.attr, data):
        return "Zapytanie nie zawiera wszystkich wymaganych wartości", 400

    if not validateDate(data['start_period']) and not validateDate(data['end_period']):
        return "Podane formaty dat nie są poprawne", 404
    
    start_period = datetime.strptime(data['start_period'] + "T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
    curr_end_period = datetime.strptime(data['end_period'] + "T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
    end_period = curr_end_period + timedelta(days=1)

    notPaidCases = NotPaidCase.query.filter(
        NotPaidCase.detect_time <= end_period, 
        NotPaidCase.detect_time >= start_period
    ).all()
    
    problematicCases = ProblematicCase.query.filter(
        ProblematicCase.detect_time >= start_period, 
        ProblematicCase.detect_time <= end_period
    ).all()

    filename = datetime.strftime(start_period, "%Y%m%d") + "-" + datetime.strftime(end_period, "%Y%m%d") + "_" + getUuid()
    report = Report(start_period, end_period, filename, curr_user['id'])

    pdfFilename = filename
    generatePDF(pdfFilename, start_period, end_period, notPaidCases, problematicCases)

    xlsxFilename = filename + '.xlsx'
    generateXLSX(filename, notPaidCases, problematicCases)
        
    db.session.add(report)
    db.session.commit()

    data = {"xslx_name": xlsxFilename, "pdf_name": pdfFilename}
    return makeResponse(data, 200)