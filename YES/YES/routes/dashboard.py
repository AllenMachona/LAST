from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.procurement import Procurement
from models.notification import Notification
from models.bidder import Bidder
from models.user import User

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def index():
    if current_user.has_role('Bidder'):
        my_bids = Bidder.query.filter_by(contact_email=current_user.email).count()
        notifications = Notification.query.filter_by(user_id=current_user.id, read=False).count()
        return render_template('dashboard.html', role='bidder', my_bids=my_bids, notifications=notifications)
    elif current_user.has_role('System Administrator'):
        total_users = User.query.count()
        total_procurements = Procurement.query.count()
        return render_template('dashboard.html', role='admin', total_users=total_users, total_procurements=total_procurements)
    else:
        active_tenders = Procurement.query.filter(Procurement.status.in_(['published','submission_open','clarification_period'])).count()
        pending_evaluations = Procurement.query.filter(Procurement.status.in_(['technical_evaluation','financial_evaluation'])).count()
        pending_approvals = Procurement.query.filter_by(status='award_pending_approval').count()
        notifications = Notification.query.filter_by(user_id=current_user.id, read=False).count()
        return render_template('dashboard.html', role='staff', active_tenders=active_tenders,
                               pending_evaluations=pending_evaluations, pending_approvals=pending_approvals, notifications=notifications)
