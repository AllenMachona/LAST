from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.evaluation_committee import EvaluationCommittee
from models.committee_member import CommitteeMember
from models.user import User
from models.procurement import Procurement
from utils.decorators import require_procurement_staff

bp = Blueprint('committee', __name__)

@bp.route('/<int:procurement_id>')
@login_required
@require_procurement_staff()
def view(procurement_id):
    committees = EvaluationCommittee.query.filter_by(procurement_id=procurement_id).all()
    return render_template('procurement/committee.html', committees=committees, procurement_id=procurement_id)

@bp.route('/<int:procurement_id>/assign', methods=['GET', 'POST'])
@login_required
@require_procurement_staff()
def assign(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    if request.method == 'POST':
        committee = EvaluationCommittee(
            procurement_id=procurement_id, evaluation_type=request.form.get('evaluation_type'),
            appointment_instrument=request.form.get('instrument'), appointed_by=current_user.id
        )
        db.session.add(committee)
        db.session.flush()
        member_ids = request.form.getlist('member_ids')
        for i, uid in enumerate(member_ids):
            role = 'chair' if i == 0 else 'member'
            db.session.add(CommitteeMember(committee_id=committee.id, user_id=int(uid), role=role))
        db.session.commit()
        flash('Committee assigned.', 'success')
        return redirect(url_for('committee.view', procurement_id=procurement_id))
    users = User.query.all()
    return render_template('procurement/assign_committee.html', procurement=procurement, users=users)
