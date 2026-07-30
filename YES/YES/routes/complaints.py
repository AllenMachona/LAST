from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models.complaint import Complaint
from models.procurement import Procurement

bp = Blueprint('complaints', __name__)

@bp.route('/<int:procurement_id>')
@login_required
def index(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    complaints = Complaint.query.filter_by(procurement_id=procurement_id).all()
    # Bidders can only see their own complaints
    if current_user.has_role('Bidder'):
        complaints = [c for c in complaints if c.complainant_id == current_user.id]
    return render_template('complaints.html', complaints=complaints, procurement_id=procurement_id)

@bp.route('/<int:procurement_id>/file', methods=['POST'])
@login_required
def file(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    if current_user.has_role('Bidder'):
        complainant_type = 'bidder'
        complainant_id = current_user.id
        complainant_name = current_user.get_full_name()
        complainant_email = current_user.email
    else:
        abort(403)  # Only bidders file complaints through this route
    complaint = Complaint(
        procurement_id=procurement_id, complainant_type=complainant_type,
        complainant_id=complainant_id, complainant_name=complainant_name,
        complainant_email=complainant_email, grounds=request.form.get('grounds'),
        relief_sought=request.form.get('relief_sought')
    )
    db.session.add(complaint)
    db.session.commit()
    flash('Complaint filed.', 'success')
    return redirect(url_for('complaints.index', procurement_id=procurement_id))
