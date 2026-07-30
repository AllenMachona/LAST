from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.audit_log import AuditLog
from utils.decorators import auditor_only

bp = Blueprint('audit', __name__)

@bp.route('/<int:procurement_id>')
@login_required
@auditor_only
def procurement_audit(procurement_id):
    logs = AuditLog.query.filter_by(procurement_id=procurement_id).order_by(AuditLog.timestamp.desc()).all()
    return render_template('audit/procurement.html', logs=logs)

@bp.route('/export/<int:procurement_id>')
@login_required
@auditor_only
def export(procurement_id):
    logs = AuditLog.query.filter_by(procurement_id=procurement_id).all()
    data = [{'timestamp': l.timestamp.isoformat(), 'user': l.user_id, 'action': l.action,
             'object': l.object_type, 'reason': l.reason} for l in logs]
    return jsonify(data)
