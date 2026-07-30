from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models.technical_evaluation import TechnicalEvaluation
from models.financial_evaluation import FinancialEvaluation
from models.bid_submission import BidSubmission
from models.procurement import Procurement
from models.evaluation_committee import EvaluationCommittee
from models.committee_member import CommitteeMember
from utils.decorators import require_evaluator, require_role

bp = Blueprint('evaluation', __name__)

def _check_committee_access(procurement_id):
    """Verify current user is on the evaluation committee for this procurement."""
    if current_user.has_role('System Administrator') or current_user.has_role('Procurement Unit'):
        return True
    committee = EvaluationCommittee.query.filter_by(procurement_id=procurement_id).first()
    if not committee:
        abort(403)
    membership = CommitteeMember.query.filter_by(committee_id=committee.id, user_id=current_user.id).first()
    if not membership or membership.status != 'active':
        abort(403)
    return True

def _check_financial_opening_authorized(procurement):
    """Ensure financial opening is approved before allowing financial evaluation."""
    if procurement.status not in ['financial_opening', 'financial_evaluation', 'award_pending_approval']:
        if not current_user.has_role('System Administrator'):
            abort(403)

@bp.route('/technical/<int:procurement_id>')
@login_required
@require_evaluator()
def technical(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    _check_committee_access(procurement_id)
    submissions = BidSubmission.query.filter_by(procurement_id=procurement_id, status='submitted').all()
    evaluations = TechnicalEvaluation.query.filter_by(procurement_id=procurement_id).all()
    return render_template('evaluation/technical.html', procurement=procurement, submissions=submissions, evaluations=evaluations)

@bp.route('/technical/<int:procurement_id>/score', methods=['POST'])
@login_required
@require_evaluator()
def score_technical(procurement_id):
    _check_committee_access(procurement_id)
    eval = TechnicalEvaluation(
        procurement_id=procurement_id, submission_id=request.form.get('submission_id'),
        evaluator_id=current_user.id, criteria_name=request.form.get('criteria_name'),
        score=request.form.get('score'), comments=request.form.get('comments'),
        is_mandatory=bool(request.form.get('is_mandatory')), passed=bool(request.form.get('passed'))
    )
    db.session.add(eval)
    db.session.commit()
    flash('Technical score recorded.', 'success')
    return redirect(url_for('evaluation.technical', procurement_id=procurement_id))

@bp.route('/financial/<int:procurement_id>')
@login_required
@require_role('Financial Evaluator', 'Procurement Unit', 'System Administrator')
def financial(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    _check_financial_opening_authorized(procurement)
    evaluations = FinancialEvaluation.query.filter_by(procurement_id=procurement_id).all()
    return render_template('evaluation/financial.html', procurement=procurement, evaluations=evaluations)

@bp.route('/consensus/<int:procurement_id>')
@login_required
@require_evaluator()
def consensus(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    _check_committee_access(procurement_id)
    return render_template('evaluation/consensus.html', procurement=procurement)

@bp.route('/reports/<int:procurement_id>')
@login_required
@require_evaluator()
def reports(procurement_id):
    procurement = Procurement.query.get_or_404(procurement_id)
    _check_committee_access(procurement_id)
    return render_template('evaluation/reports.html', procurement=procurement)
