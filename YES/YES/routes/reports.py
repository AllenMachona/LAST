from flask import Blueprint, render_template, Response
from flask_login import login_required
from models.procurement import Procurement
from utils.decorators import require_procurement_staff
import csv
import io

bp = Blueprint('reports', __name__)

@bp.route('/procurements')
@login_required
@require_procurement_staff()
def procurements():
    procs = Procurement.query.all()
    return render_template('reports/procurements.html', procurements=procs)

@bp.route('/export/csv')
@login_required
@require_procurement_staff()
def export_csv():
    procs = Procurement.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Tender Number', 'Title', 'Status', 'Category', 'Value'])
    for p in procs:
        writer.writerow([p.tender_number, p.title, p.status, p.category, p.estimated_value])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=procurements.csv'})
