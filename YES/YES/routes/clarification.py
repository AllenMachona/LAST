from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models.clarification import Clarification
from models.procurement import Procurement
from datetime import datetime
import pytz

bp = Blueprint('clarification', __name__)

@bp.route('/<int:procurement_id>')
@login_required
def index(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    # Bidders: only if procurement is published or later
    if current_user.has_role('Bidder') and procurement.status in ['draft', 'internal_review', 'approved_for_publication']:
        abort(403)
    clarifications = Clarification.query.filter_by(procurement_id=procurement_id).all()
    return render_template('clarifications.html', clarifications=clarifications, procurement_id=procurement_id)

@bp.route('/<int:procurement_id>/ask', methods=['POST'])
@login_required
def ask(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    if current_user.has_role('Bidder'):
        # Bidders can only ask during clarification/submission period
        if procurement.status not in ['published', 'clarification_period', 'submission_open']:
            abort(403)
        requester_type = 'bidder'
        requester_id = current_user.id
    else:
        requester_type = 'procurement_unit'
        requester_id = current_user.id
    c = Clarification(
        procurement_id=procurement_id, requester_type=requester_type, requester_id=requester_id,
        question=request.form.get('question'), anonymous=bool(request.form.get('anonymous'))
    )
    db.session.add(c)
    db.session.commit()
    flash('Question submitted.', 'success')
    return redirect(url_for('clarification.index', procurement_id=procurement_id))

@bp.route('/<int:id>/respond', methods=['POST'])
@login_required
def respond(id):
    c = Clarification.query.get_or_404(id)
    # Only procurement staff or committee secretary can respond
    if current_user.has_role('Bidder'):
        abort(403)
    c.response = request.form.get('response')
    c.responded_by = current_user.id
    c.responded_at = datetime.now(pytz.timezone('Africa/Gaborone'))
    c.status = 'responded'
    if request.form.get('publish'):
        c.is_public = True
        c.published_at = datetime.now(pytz.timezone('Africa/Gaborone'))
        c.status = 'published'
    db.session.commit()
    flash('Response saved.', 'success')
    return redirect(url_for('clarification.index', procurement_id=c.procurement_id))
