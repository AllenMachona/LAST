from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models.award import Award
from models.procurement import Procurement
from utils.decorators import require_role, require_approver
from datetime import datetime, timedelta
import pytz

bp = Blueprint('award', __name__)

@bp.route('/<int:procurement_id>')
@login_required
def index(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    # Bidders: only see award after it's published
    if current_user.has_role('Bidder') and procurement.status not in ['award_published', 'cooling_off', 'ready_for_contract', 'archived']:
        abort(403)
    awards = Award.query.filter_by(procurement_id=procurement_id).all()
    return render_template('award.html', awards=awards, procurement=procurement)

@bp.route('/<int:procurement_id>/recommend', methods=['POST'])
@login_required
@require_role('Procurement Unit', 'System Administrator')
def recommend(procurement_id):
    award = Award(
        procurement_id=procurement_id, submission_id=request.form.get('submission_id'),
        bidder_id=request.form.get('bidder_id'), contract_amount=request.form.get('contract_amount'),
        recommendation_by=current_user.id, recommended_at=datetime.now(pytz.timezone('Africa/Gaborone'))
    )
    db.session.add(award)
    db.session.commit()
    flash('Award recommendation created.', 'success')
    return redirect(url_for('award.index', procurement_id=procurement_id))

@bp.route('/<int:award_id>/approve', methods=['POST'])
@login_required
@require_approver()
def approve(award_id):
    award = Award.query.get_or_404(award_id)
    # Segregation: cannot approve your own recommendation
    if award.recommendation_by == current_user.id:
        flash('You cannot approve your own recommendation.', 'danger')
        return redirect(url_for('award.index', procurement_id=award.procurement_id))
    award.ao_approved = True
    award.ao_approved_by = current_user.id
    award.ao_approved_at = datetime.now(pytz.timezone('Africa/Gaborone'))
    award.status = 'approved'
    db.session.commit()
    flash('Award approved.', 'success')
    return redirect(url_for('award.index', procurement_id=award.procurement_id))

@bp.route('/<int:award_id>/publish', methods=['POST'])
@login_required
@require_approver()
def publish(award_id):
    award = Award.query.get_or_404(award_id)
    award.published = True
    award.published_at = datetime.now(pytz.timezone('Africa/Gaborone'))
    award.cooling_off_started = True
    award.cooling_off_start = datetime.now(pytz.timezone('Africa/Gaborone'))
    award.cooling_off_end = award.cooling_off_start + timedelta(days=10)
    award.status = 'cooling_off'
    db.session.commit()
    flash('Award published. Cooling-off period started.', 'success')
    return redirect(url_for('award.index', procurement_id=award.procurement_id))
