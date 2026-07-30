from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.procurement import Procurement
from models.workspace import Workspace
from models.ppra_code import PPRACode
from models.bid_submission import BidSubmission
from services.audit_service import log_audit
from services.workflow_service import WorkflowService
from utils.tender_number import generate_tender_number
from utils.decorators import require_role, require_procurement_staff
from datetime import datetime
import pytz

bp = Blueprint('procurement', __name__)

@bp.route('/list')
@login_required
def list_tenders():
    if current_user.has_role('Bidder'):
        # Bidders see only published or later
        tenders = Procurement.query.filter(
            Procurement.status.in_(['published', 'submission_open', 'closed', 'technical_opening', 
                                   'compliance_evaluation', 'technical_evaluation', 'technical_outcome_approved',
                                   'financial_opening', 'financial_evaluation', 'award_pending_approval',
                                   'award_published', 'cooling_off', 'ready_for_contract'])
        ).order_by(Procurement.created_at.desc()).all()
    else:
        # Staff see all
        tenders = Procurement.query.order_by(Procurement.created_at.desc()).all()
    return render_template('procurement/list.html', tenders=tenders)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@require_procurement_staff()
def create():
    if request.method == 'POST':
        procurement = Procurement(
            tender_number=generate_tender_number(),
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            procurement_method=request.form.get('procurement_method'),
            submission_method=request.form.get('submission_method', 'single_envelope'),
            estimated_value=request.form.get('estimated_value') or None,
            currency=request.form.get('currency', 'BWP'),
            funding_source=request.form.get('funding_source'),
            ppra_code=request.form.get('ppra_code'),
            closing_date=datetime.strptime(request.form.get('closing_date'), '%Y-%m-%dT%H:%M') if request.form.get('closing_date') else None,
            created_by=current_user.id
        )
        db.session.add(procurement)
        db.session.flush()
        workspace = Workspace(procurement_id=procurement.id, workspace_name=f"WS-{procurement.tender_number}")
        db.session.add(workspace)
        db.session.commit()
        log_audit(current_user.id, 'procurement_created', 'Procurement', procurement.id, procurement.id)
        flash('Procurement created successfully.', 'success')
        return redirect(url_for('procurement.details', id=procurement.id))
    ppra_codes = PPRACode.query.filter_by(is_active=True).all()
    return render_template('procurement/create.html', ppra_codes=ppra_codes)

@bp.route('/<int:id>')
@login_required
def details(id):
    procurement = Procurement.query.get_or_404(id)
    # Bidders can only view published or later status
    if current_user.has_role('Bidder') and procurement.status in ['draft', 'internal_review', 'approved_for_publication']:
        abort(403)
    return render_template('procurement/details.html', procurement=procurement)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@require_procurement_staff()
def edit(id):
    procurement = Procurement.query.get_or_404(id)
    if request.method == 'POST':
        procurement.title = request.form.get('title')
        procurement.description = request.form.get('description')
        procurement.estimated_value = request.form.get('estimated_value') or None
        db.session.commit()
        flash('Procurement updated.', 'success')
        return redirect(url_for('procurement.details', id=id))
    return render_template('procurement/edit.html', procurement=procurement)

@bp.route('/<int:id>/send-review', methods=['POST'])
@login_required
@require_procurement_staff()
def send_review(id):
    procurement = Procurement.query.get_or_404(id)
    ws = WorkflowService(procurement)
    if ws.can_transition('internal_review'):
        ws.transition('internal_review', current_user.id)
        flash('Sent to internal review.', 'success')
    else:
        flash('Cannot send to review from current status.', 'danger')
    return redirect(url_for('procurement.details', id=id))

@bp.route('/<int:id>/approve-publication', methods=['POST'])
@login_required
@require_procurement_staff()
def approve_publication(id):
    procurement = Procurement.query.get_or_404(id)
    ws = WorkflowService(procurement)
    if ws.can_transition('approved_for_publication'):
        ws.transition('approved_for_publication', current_user.id)
        flash('Approved for publication.', 'success')
    else:
        flash('Cannot approve from current status.', 'danger')
    return redirect(url_for('procurement.details', id=id))

@bp.route('/<int:id>/publish', methods=['POST'])
@login_required
@require_procurement_staff()
def publish(id):
    procurement = Procurement.query.get_or_404(id)
    ws = WorkflowService(procurement)
    if ws.can_transition('published'):
        ws.transition('published', current_user.id)
        flash('Procurement published.', 'success')
    else:
        flash('Cannot publish from current status.', 'danger')
    return redirect(url_for('procurement.details', id=id))

@bp.route('/<int:id>/open-submission', methods=['POST'])
@login_required
@require_procurement_staff()
def open_submission(id):
    procurement = Procurement.query.get_or_404(id)
    ws = WorkflowService(procurement)
    if ws.can_transition('submission_open'):
        ws.transition('submission_open', current_user.id)
        flash('Submissions are now open.', 'success')
    else:
        flash('Cannot open submissions from current status.', 'danger')
    return redirect(url_for('procurement.details', id=id))

@bp.route('/<int:id>/close-submission', methods=['POST'])
@login_required
@require_procurement_staff()
def close_submission(id):
    procurement = Procurement.query.get_or_404(id)
    ws = WorkflowService(procurement)
    if ws.can_transition('closed'):
        ws.transition('closed', current_user.id)
        flash('Submissions closed.', 'success')
    else:
        flash('Cannot close submissions from current status.', 'danger')
    return redirect(url_for('procurement.details', id=id))

@bp.route('/<int:id>/workspace')
@login_required
def workspace(id):
    procurement = Procurement.query.get_or_404(id)
    # Bidders: only if they are registered for this procurement
    if current_user.has_role('Bidder'):
        from models.bidder import Bidder
        bidder = Bidder.query.filter_by(procurement_id=id, contact_email=current_user.email).first()
        if not bidder:
            abort(403)
    return render_template('procurement/workspace.html', procurement=procurement)

@bp.route('/<int:id>/timeline')
@login_required
def timeline(id):
    procurement = Procurement.query.get_or_404(id)
    if current_user.has_role('Bidder') and procurement.status in ['draft', 'internal_review', 'approved_for_publication']:
        abort(403)
    return render_template('procurement/timeline.html', procurement=procurement)

@bp.route('/<int:id>/history')
@login_required
def history(id):
    procurement = Procurement.query.get_or_404(id)
    return render_template('procurement/history.html', procurement=procurement)
